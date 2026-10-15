package net.azli.mypersonalquran;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.net.Uri;

import com.google.mlkit.vision.common.InputImage;
import com.google.mlkit.vision.text.TextRecognition;
import com.google.mlkit.vision.text.latin.TextRecognizerOptions;
import com.googlecode.tesseract.android.TessBaseAPI;

import org.json.JSONObject;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * Reads the text in a photo or screenshot, on the phone (no internet).
 * Arabic: Tesseract with the Arabic model (tessdata_best) packed in the APK.
 * Malay / English: Google ML Kit Latin text recognition (bundled model).
 */
final class ScanOcr {
    interface Done { void done(String json); }

    private ScanOcr() { }

    static void run(final Context ctx, final Uri uri, final String lang, final Done cb) {
        new Thread(() -> {
            Bitmap bmp;
            try { bmp = load(ctx, uri, "ar".equals(lang) ? 2600 : 2000); }
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
        TessBaseAPI tess = null;
        try {
            File base = new File(ctx.getFilesDir(), "tess");
            File dir = new File(base, "tessdata"); dir.mkdirs();
            File f = new File(dir, "ara.traineddata");
            long want = -1;
            try (android.content.res.AssetFileDescriptor fd = ctx.getAssets().openFd("tessdata/ara.traineddata")) { want = fd.getLength(); } catch (Exception ignored) { }
            if (!f.exists() || (want > 0 && f.length() != want)) {
                File tmp = new File(dir, "ara.tmp");
                try (InputStream in = ctx.getAssets().open("tessdata/ara.traineddata"); OutputStream out = new FileOutputStream(tmp)) {
                    byte[] buf = new byte[65536]; int n; while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
                }
                if (!tmp.renameTo(f)) return err("Could not prepare the Arabic reader.");
            }
            tess = new TessBaseAPI();
            if (!tess.init(base.getAbsolutePath(), "ara")) return err("Could not start the Arabic reader.");
            tess.setPageSegMode(TessBaseAPI.PageSegMode.PSM_AUTO);
            tess.setImage(bmp);
            String text = tess.getUTF8Text();
            return ok(text == null ? "" : text, "ar");
        } catch (Throwable e) {
            return err("Arabic reading failed.");
        } finally {
            if (tess != null) try { tess.recycle(); } catch (Throwable ignored) { }
        }
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
