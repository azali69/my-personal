package net.azli.mypersonalquran;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.net.Uri;

import com.google.mlkit.vision.common.InputImage;
import com.google.mlkit.vision.text.TextRecognition;
import com.google.mlkit.vision.text.latin.TextRecognizerOptions;

import org.json.JSONObject;

import java.io.InputStream;

/**
 * Reads the text in a photo or screenshot, on the phone (no internet).
 * Arabic: ArabicOcr (PaddleOCR line detector + EasyOCR Arabic recogniser, ONNX, packed in the APK).
 * Malay / English: Google ML Kit Latin text recognition (bundled model).
 */
final class ScanOcr {
    interface Done { void done(String json); }

    private ScanOcr() { }

    static void run(final Context ctx, final Uri uri, final String lang, final Done cb) {
        new Thread(() -> {
            Bitmap bmp;
            try { bmp = load(ctx, uri, 2000); }
            catch (Throwable e) { cb.done(err("Could not open the picture.")); return; }
            if (bmp == null) { cb.done(err("Could not open the picture.")); return; }
            if ("ar".equals(lang)) {
                cb.done(arabic(ctx, bmp));
            } else {
                final Bitmap b = bmp;
                try {
                    TextRecognition.getClient(TextRecognizerOptions.DEFAULT_OPTIONS)
                        .process(InputImage.fromBitmap(b, 0))
                        .addOnSuccessListener(t -> cb.done(ok(t.getText(), lang)))
                        .addOnFailureListener(e -> cb.done(err("Text recognition failed.")));
                } catch (Throwable e) { cb.done(err("Text recognition failed.")); }
            }
        }, "scan-ocr").start();
    }

    private static String arabic(Context ctx, Bitmap bmp) {
        if (!ArabicOcr.ready(ctx)) return "{\"needReader\":true}";
        try { return ok(ArabicOcr.read(ctx, bmp), "ar"); }
        catch (Throwable e) { return err("Arabic reading failed. Try \"Read with Google Lens\"."); }
    }

    /** Opens the picture, turns it upright (camera EXIF) and scales the long side down to max. */
    static Bitmap load(Context ctx, Uri uri, int max) throws Exception {
        BitmapFactory.Options o = new BitmapFactory.Options(); o.inJustDecodeBounds = true;
        try (InputStream in = ctx.getContentResolver().openInputStream(uri)) { BitmapFactory.decodeStream(in, null, o); }
        int s = 1; while (Math.max(o.outWidth, o.outHeight) / (s * 2) >= max) s *= 2;
        BitmapFactory.Options o2 = new BitmapFactory.Options(); o2.inSampleSize = s; o2.inPreferredConfig = Bitmap.Config.ARGB_8888;
        Bitmap b;
        try (InputStream in = ctx.getContentResolver().openInputStream(uri)) { b = BitmapFactory.decodeStream(in, null, o2); }
        if (b == null) return null;
        int rot = 0;
        try (InputStream in = ctx.getContentResolver().openInputStream(uri)) {
            android.media.ExifInterface ex = new android.media.ExifInterface(in);
            int or = ex.getAttributeInt(android.media.ExifInterface.TAG_ORIENTATION, 1);
            rot = or == 6 ? 90 : or == 3 ? 180 : or == 8 ? 270 : 0;
        } catch (Throwable ignored) { }
        float k = Math.min(1f, max / (float) Math.max(b.getWidth(), b.getHeight()));
        if (rot != 0 || k < 1f) {
            Matrix m = new Matrix(); m.postScale(k, k); if (rot != 0) m.postRotate(rot);
            Bitmap r = Bitmap.createBitmap(b, 0, 0, b.getWidth(), b.getHeight(), m, true);
            if (r != b) b.recycle();
            b = r;
        }
        return b;
    }

    private static String ok(String text, String lang) {
        try { return new JSONObject().put("text", text).put("lang", lang).toString(); } catch (Exception e) { return err("?"); }
    }
    static String err(String msg) {
        try { return new JSONObject().put("error", msg).toString(); } catch (Exception e) { return "{\"error\":\"?\"}"; }
    }
}
