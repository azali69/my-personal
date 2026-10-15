package net.azli.mypersonalquran;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Color;

import ai.onnxruntime.OnnxTensor;
import ai.onnxruntime.OrtEnvironment;
import ai.onnxruntime.OrtSession;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.FloatBuffer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Arabic text reading on the phone, in two steps (both ONNX models packed in the APK):
 *  1. find the lines of text: PaddleOCR's text detector (PP-OCRv4 det, DB), from RapidOCR;
 *  2. read each line: EasyOCR's Arabic recogniser (arabic_g1, CRNN + CTC), exported to ONNX.
 * Tested on photos of screens, screenshots of the mushaf and hadith pages (15 Oct 2026): it reads Qur'an script with
 * harakat far better than Tesseract.
 */
final class ArabicOcr {
    private static OrtEnvironment env;
    private static OrtSession det, rec;
    private static String[] chars;            // index 0 = CTC blank
    private static boolean[] ignore;

    private ArabicOcr() { }

    static final String BASE = "https://github.com/azali69/my-personal/releases/download/ocr-models-1/";
    static final String[] FILES = {"det.onnx", "ar_rec.onnx", "ar_rec.json"};
    static final long[] SIZES = {4745517L, 54000956L, 374L};
    static java.io.File dir(Context c) { return new java.io.File(c.getFilesDir(), "ocr"); }
    /** The reader is downloaded once on first use (about 59 MB) and kept in the app's own storage. */
    static boolean ready(Context c) {
        for (int i = 0; i < FILES.length; i++) { java.io.File f = new java.io.File(dir(c), FILES[i]); if (!f.exists() || f.length() != SIZES[i]) return false; }
        return true;
    }
    interface Progress { void at(int pct); }
    static void download(Context c, Progress p) throws Exception {
        java.io.File d = dir(c); d.mkdirs(); long total = 0, done = 0; for (long s : SIZES) total += s;
        for (int i = 0; i < FILES.length; i++) {
            java.io.File f = new java.io.File(d, FILES[i]);
            if (f.exists() && f.length() == SIZES[i]) { done += SIZES[i]; continue; }
            java.io.File tmp = new java.io.File(d, FILES[i] + ".part");
            java.net.HttpURLConnection h = (java.net.HttpURLConnection) new java.net.URL(BASE + FILES[i]).openConnection();
            h.setInstanceFollowRedirects(true); h.setConnectTimeout(20000); h.setReadTimeout(30000);
            int code = h.getResponseCode(); if (code != 200) throw new Exception("HTTP " + code);
            try (InputStream in = h.getInputStream(); java.io.OutputStream out = new java.io.FileOutputStream(tmp)) {
                byte[] b = new byte[1 << 16]; int n; int last = -1;
                while ((n = in.read(b)) > 0) { out.write(b, 0, n); done += n; int pct = (int) (done * 100 / total); if (pct != last) { last = pct; p.at(pct); } }
            } finally { h.disconnect(); }
            if (tmp.length() != SIZES[i] || !tmp.renameTo(f)) { tmp.delete(); throw new Exception("incomplete " + FILES[i]); }
        }
    }

    private static byte[] asset(Context c, String name) throws Exception {
        try (InputStream in = new java.io.FileInputStream(new java.io.File(dir(c), name.replace("ocr/", "")))) {
            ByteArrayOutputStream bo = new ByteArrayOutputStream(); byte[] b = new byte[1 << 16]; int n;
            while ((n = in.read(b)) > 0) bo.write(b, 0, n); return bo.toByteArray();
        }
    }

    private static synchronized void init(Context c) throws Exception {
        if (rec != null) return;
        env = OrtEnvironment.getEnvironment();
        OrtSession.SessionOptions o = new OrtSession.SessionOptions();
        o.setIntraOpNumThreads(Math.max(1, Math.min(4, Runtime.getRuntime().availableProcessors())));
        det = env.createSession(asset(c, "ocr/det.onnx"), o);
        rec = env.createSession(asset(c, "ocr/ar_rec.onnx"), o);
        JSONObject meta = new JSONObject(new String(asset(c, "ocr/ar_rec.json"), "UTF-8"));
        String cs = meta.getString("chars"), ig = meta.getString("ignore");
        int[] cps = cs.codePoints().toArray();
        chars = new String[cps.length + 1]; chars[0] = "";
        for (int i = 0; i < cps.length; i++) chars[i + 1] = new String(Character.toChars(cps[i]));
        Set<Integer> igs = new HashSet<>(); ig.codePoints().forEach(igs::add);
        ignore = new boolean[chars.length];
        for (int i = 0; i < cps.length; i++) ignore[i + 1] = igs.contains(cps[i]);
    }

    /** Reads the Arabic in the picture; lines top to bottom, right to left within a line. */
    static String read(Context c, Bitmap bmp) throws Exception {
        init(c);
        List<float[]> boxes = detect(bmp);
        List<List<float[]>> rows = order(boxes);
        StringBuilder out = new StringBuilder();
        for (List<float[]> row : rows) {
            StringBuilder line = new StringBuilder();
            for (float[] b : row) { String t = recognize(bmp, b); if (!t.isEmpty()) { if (line.length() > 0) line.append(' '); line.append(t); } }
            if (line.length() > 0) out.append(line).append('\n');
        }
        return out.toString().trim();
    }

    private static List<float[]> detect(Bitmap bmp) throws Exception {
        int W = bmp.getWidth(), H = bmp.getHeight();
        float s = Math.min(1f, 960f / Math.max(W, H));
        int w2 = Math.max(32, Math.round(W * s / 32f) * 32), h2 = Math.max(32, Math.round(H * s / 32f) * 32);
        Bitmap sm = Bitmap.createScaledBitmap(bmp, w2, h2, true);
        int[] px = new int[w2 * h2]; sm.getPixels(px, 0, w2, 0, 0, w2, h2); if (sm != bmp) sm.recycle();
        float[] in = new float[3 * w2 * h2]; int pl = w2 * h2;
        float[] mean = {0.485f, 0.456f, 0.406f}, std = {0.229f, 0.224f, 0.225f};
        for (int i = 0; i < pl; i++) { int p = px[i];
            in[i] = (((p >> 16) & 255) / 255f - mean[0]) / std[0];
            in[pl + i] = (((p >> 8) & 255) / 255f - mean[1]) / std[1];
            in[2 * pl + i] = ((p & 255) / 255f - mean[2]) / std[2]; }
        float[] prob;
        try (OnnxTensor t = OnnxTensor.createTensor(env, FloatBuffer.wrap(in), new long[]{1, 3, h2, w2});
             OrtSession.Result r = det.run(Collections.singletonMap(det.getInputNames().iterator().next(), t))) {
            float[][][][] y = (float[][][][]) r.get(0).getValue();
            prob = new float[pl]; for (int yy = 0; yy < h2; yy++) System.arraycopy(y[0][0][yy], 0, prob, yy * w2, w2);
        }
        // connected regions of the probability map above 0.3 (4-neighbour), kept if their mean is at least 0.6
        int[] lab = new int[pl]; int[] stack = new int[pl]; List<float[]> boxes = new ArrayList<>(); int id = 0;
        for (int i = 0; i < pl; i++) {
            if (lab[i] != 0 || prob[i] <= 0.3f) continue;
            id++; int sp = 0; stack[sp++] = i; lab[i] = id;
            int x0 = w2, y0 = h2, x1 = 0, y1 = 0; double sum = 0; int cnt = 0;
            while (sp > 0) { int k = stack[--sp]; int x = k % w2, y = k / w2;
                sum += prob[k]; cnt++; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
                int[] nb = {k - 1, k + 1, k - w2, k + w2};
                for (int q = 0; q < 4; q++) { int m = nb[q];
                    if (m < 0 || m >= pl) continue; if ((q == 0 && x == 0) || (q == 1 && x == w2 - 1)) continue;
                    if (lab[m] == 0 && prob[m] > 0.3f) { lab[m] = id; stack[sp++] = m; } } }
            int bw = x1 - x0 + 1, bh = y1 - y0 + 1;
            if (bw < 3 || bh < 3 || sum / cnt < 0.6) continue;
            float d = bw * bh * 1.5f / (2f * (bw + bh));             // DB "unclip" of a rectangle
            float sx = W / (float) w2, sy = H / (float) h2;
            boxes.add(new float[]{Math.max(0, (x0 - d) * sx), Math.max(0, (y0 - d) * sy), Math.min(W, (x1 + 1 + d) * sx), Math.min(H, (y1 + 1 + d) * sy)});
        }
        return boxes;
    }

    private static List<List<float[]>> order(List<float[]> boxes) {
        Collections.sort(boxes, (a, b) -> Float.compare(a[1] + a[3], b[1] + b[3]));
        List<List<float[]>> rows = new ArrayList<>(); List<Float> centres = new ArrayList<>();
        for (float[] b : boxes) { float c = (b[1] + b[3]) / 2f;
            int last = rows.size() - 1;
            if (last >= 0 && Math.abs(c - centres.get(last)) < 0.5f * (b[3] - b[1])) rows.get(last).add(b);
            else { List<float[]> r = new ArrayList<>(); r.add(b); rows.add(r); centres.add(c); } }
        for (List<float[]> r : rows) Collections.sort(r, (a, b) -> Float.compare(b[2], a[2]));   // right to left
        return rows;
    }

    private static String recognize(Bitmap bmp, float[] b) throws Exception {
        int x0 = Math.round(b[0]), y0 = Math.round(b[1]), x1 = Math.round(b[2]), y1 = Math.round(b[3]);
        int cw = x1 - x0, ch = y1 - y0; if (cw < 4 || ch < 4) return "";
        int w = Math.max(8, (int) Math.ceil(64.0 * cw / ch)); if (w > 2400) w = 2400;
        Bitmap crop = Bitmap.createBitmap(bmp, x0, y0, cw, ch);
        Bitmap sc = Bitmap.createScaledBitmap(crop, w, 64, true); if (crop != bmp && crop != sc) crop.recycle();
        int[] px = new int[w * 64]; sc.getPixels(px, 0, w, 0, 0, w, 64); sc.recycle();
        float[] in = new float[w * 64];
        for (int i = 0; i < px.length; i++) { int p = px[i];
            float g = (0.299f * Color.red(p) + 0.587f * Color.green(p) + 0.114f * Color.blue(p)) / 255f;   // as PIL's "L"
            in[i] = (g - 0.5f) / 0.5f; }
        StringBuilder s = new StringBuilder();
        try (OnnxTensor t = OnnxTensor.createTensor(env, FloatBuffer.wrap(in), new long[]{1, 1, 64, w});
             OrtSession.Result r = rec.run(Collections.singletonMap("x", t))) {
            float[][][] y = (float[][][]) r.get(0).getValue();
            int prev = 0;
            for (float[] row : y[0]) { int best = 0; float bv = -Float.MAX_VALUE;
                for (int k = 0; k < row.length; k++) { if (k > 0 && k < ignore.length && ignore[k]) continue; if (row[k] > bv) { bv = row[k]; best = k; } }
                if (best != prev && best != 0 && best < chars.length) s.append(chars[best]);
                prev = best; }
        }
        return logical(s.toString());
    }

    /** The model reads left to right; Arabic is stored right to left: reverse, then put Latin letters and digits back in order. */
    static String logical(String s) {
        int[] cp = new StringBuilder(s).reverse().toString().codePoints().toArray();
        StringBuilder out = new StringBuilder(), run = new StringBuilder();
        for (int c : cp) {
            if (c < 128 && Character.isLetterOrDigit(c)) run.appendCodePoint(c);
            else { if (run.length() > 0) { out.append(run.reverse()); run.setLength(0); } out.appendCodePoint(c); }
        }
        if (run.length() > 0) out.append(run.reverse());
        return out.toString();
    }
}
