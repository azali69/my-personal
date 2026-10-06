package net.azli.mypersonalquran;

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.media.AudioDeviceInfo;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.media.audiofx.AutomaticGainControl;
import android.media.audiofx.NoiseSuppressor;
import android.os.ParcelFileDescriptor;
import android.os.SystemClock;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.view.WindowManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.webkit.WebViewAssetLoader;

import org.json.JSONObject;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

import java.util.ArrayList;

/**
 * Hosts the My Personal Quran web app from the APK's own assets (works offline)
 * and gives it Android's speech recogniser, because WebView has no Web Speech API.
 */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final int REQ_MIC = 7;
    private static final String QUL_HOST = "static-cdn.tarteel.ai";

    /** Printed-page fonts from QUL: downloaded once, then served from the phone so pages open offline. */
    private WebResourceResponse qulFont(Uri u) {
        try {
            String path = u.getPath();
            if (path == null || !path.startsWith("/qul/fonts/")) return null;
            File f = new File(getFilesDir(), "qul" + path);
            if (!f.exists()) {
                File dir = f.getParentFile();
                if (dir != null) dir.mkdirs();
                HttpURLConnection c = (HttpURLConnection) new URL(u.toString()).openConnection();
                c.setConnectTimeout(15000);
                c.setReadTimeout(30000);
                if (c.getResponseCode() != 200) { c.disconnect(); return null; }
                File tmp = new File(f.getPath() + ".part");
                try (InputStream in = c.getInputStream(); OutputStream out = new FileOutputStream(tmp)) {
                    byte[] buf = new byte[16384];
                    int n;
                    while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
                }
                c.disconnect();
                if (!tmp.renameTo(f)) return null;
            }
            Map<String, String> h = new HashMap<>();
            h.put("Access-Control-Allow-Origin", "*");
            h.put("Cache-Control", "max-age=31536000");
            String mime = path.endsWith(".woff") ? "font/woff" : "font/woff2";
            return new WebResourceResponse(mime, null, 200, "OK", h, new FileInputStream(f));
        } catch (Exception e) {
            return null;
        }
    }

    private WebView web;
    private volatile String insets = "";
    private static final int BASE_UI = View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION;
    private SpeechRecognizer recognizer;
    private String pendingLang;

    /* Quiet-voice boost (Android 13+): we record the microphone ourselves, raise quiet speech, and hand the
       stream to the speech recognizer. If the phone's recognizer does not accept it, we go back to its own microphone. */
    private boolean boostFailed = false, usingBoost = false;
    private String lastLang = "ar-SA";
    private long boostStart = 0;
    private int boostNoSpeech = 0;
    private volatile boolean pumping = false;
    private volatile float pumpPeakRms = 0;
    private AudioRecord pumpRec;
    private Thread pumpThread;
    private ParcelFileDescriptor pumpRead;

    /* Microphone choices from the page: sensitivity (0 normal, 1 high, 2 maximum) and Bluetooth headset use. */
    private volatile int micLevel = 1;
    private volatile boolean micNoisy = false;
    private boolean useBt = true, btOn = false, wantListen = false;
    private AudioDeviceInfo btIn;
    private static final float[] MAX_GAIN = {3f, 6f, 12f}, TARGET = {2400f, 2800f, 3400f}, GATE = {120f, 80f, 45f};

    /** A Bluetooth headset microphone, if one is connected. */
    private AudioDeviceInfo findBtMic(AudioManager am) {
        for (AudioDeviceInfo d : am.getDevices(AudioManager.GET_DEVICES_INPUTS)) {
            int t = d.getType();
            if (t == AudioDeviceInfo.TYPE_BLUETOOTH_SCO || (Build.VERSION.SDK_INT >= 31 && t == AudioDeviceInfo.TYPE_BLE_HEADSET)) return d;
        }
        return null;
    }

    /** Routes recording to the Bluetooth headset. Returns true if the route was just switched on (it needs a moment to connect). */
    private boolean btRouteOn() {
        AudioManager am = (AudioManager) getSystemService(AUDIO_SERVICE);
        if (am == null || !useBt) { btRouteOff(); return false; }
        AudioDeviceInfo mic = findBtMic(am);
        if (mic == null) { btRouteOff(); return false; }
        btIn = mic;
        if (btOn) return false;
        try {
            am.setMode(AudioManager.MODE_IN_COMMUNICATION);
            if (Build.VERSION.SDK_INT >= 31) {
                for (AudioDeviceInfo d : am.getAvailableCommunicationDevices()) {
                    int t = d.getType();
                    if (t == AudioDeviceInfo.TYPE_BLUETOOTH_SCO || t == AudioDeviceInfo.TYPE_BLE_HEADSET) { am.setCommunicationDevice(d); break; }
                }
            } else {
                am.startBluetoothSco();
                am.setBluetoothScoOn(true);
            }
            btOn = true;
            return true;
        } catch (Exception e) { btRouteOff(); return false; }
    }

    private void btRouteOff() {
        btIn = null;
        if (!btOn) return;
        btOn = false;
        AudioManager am = (AudioManager) getSystemService(AUDIO_SERVICE);
        if (am == null) return;
        try {
            if (Build.VERSION.SDK_INT >= 31) am.clearCommunicationDevice();
            else { am.setBluetoothScoOn(false); am.stopBluetoothSco(); }
            am.setMode(AudioManager.MODE_NORMAL);
        } catch (Exception ignored) { }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (Build.VERSION.SDK_INT >= 28) {
            WindowManager.LayoutParams lp = getWindow().getAttributes();
            lp.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            getWindow().setAttributes(lp);
        }
        getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.parseColor("#f4efe2")));
        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#f4efe2"));
        setContentView(web);
        // Draw edge to edge all the time, so the page never resizes when the system bars hide or show.
        // The page keeps fixed margins for the bars instead (sent to it as CSS pixels below).
        if (Build.VERSION.SDK_INT >= 30) getWindow().setDecorFitsSystemWindows(false);
        else getWindow().getDecorView().setSystemUiVisibility(BASE_UI);
        web.setOnApplyWindowInsetsListener((v, ins) -> {
            float d = getResources().getDisplayMetrics().density;
            int t, r, b, l, k;
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets i = ins.getInsetsIgnoringVisibility(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                t = i.top; r = i.right; b = i.bottom; l = i.left;
                k = ins.getInsets(WindowInsets.Type.ime()).bottom;   // the on-screen keyboard (0 when hidden)
            } else {
                k = Math.max(0, ins.getSystemWindowInsetBottom() - ins.getStableInsetBottom());
                t = ins.getStableInsetTop(); r = ins.getStableInsetRight(); b = ins.getStableInsetBottom(); l = ins.getStableInsetLeft();
                if (Build.VERSION.SDK_INT >= 28 && ins.getDisplayCutout() != null) {
                    android.view.DisplayCutout c = ins.getDisplayCutout();
                    t = Math.max(t, c.getSafeInsetTop()); r = Math.max(r, c.getSafeInsetRight());
                    b = Math.max(b, c.getSafeInsetBottom()); l = Math.max(l, c.getSafeInsetLeft());
                }
            }
            String now = Math.round(t / d) + "," + Math.round(r / d) + "," + Math.round(b / d) + "," + Math.round(l / d) + "," + Math.round(k / d);
            if (!now.equals(insets)) { insets = now; web.evaluateJavascript("window.__insets && window.__insets()", null); }
            return ins;
        });

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(true);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        // The app has its own text-size setting: ignore the phone's system font size so pages look the same on every phone
        s.setTextZoom(100);

        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
                .setDomain(HOST)
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri u = request.getUrl();
                if (QUL_HOST.equals(u.getHost()) && "GET".equals(request.getMethod())) return qulFont(u);
                return loader.shouldInterceptRequest(u);
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri u = request.getUrl();
                if (HOST.equals(u.getHost())) return false;
                try { startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (Exception ignored) { }
                return true;
            }
        });
        web.addJavascriptInterface(new SpeechBridge(), "AndroidSpeech");
        web.loadUrl("https://" + HOST + "/assets/index.html");
    }

    /* ---------------- Speech bridge ---------------- */

    private void emit(String fn, JSONObject arg) {
        final String js = "window.__androidSpeech && window.__androidSpeech." + fn + "(" + (arg == null ? "" : arg.toString()) + ")";
        runOnUiThread(() -> web.evaluateJavascript(js, null));
    }

    private void emitError(String code) {
        try { JSONObject o = new JSONObject(); o.put("error", code); emit("onerror", o); } catch (Exception ignored) { }
    }

    private class SpeechBridge {
        @JavascriptInterface
        public boolean isAvailable() {
            return SpeechRecognizer.isRecognitionAvailable(MainActivity.this);
        }

        @JavascriptInterface
        public void start(final String lang) {
            runOnUiThread(() -> {
                wantListen = true;
                if (Build.VERSION.SDK_INT >= 23 &&
                        checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                    pendingLang = lang;
                    requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, REQ_MIC);
                    return;
                }
                startRecognizer(lang);
            });
        }

        @JavascriptInterface
        public void stop() {
            runOnUiThread(() -> { wantListen = false; if (recognizer != null) recognizer.stopListening(); btRouteOff(); });
        }

        /** Fixed margins for the status bar, navigation bar and camera cutout, plus the keyboard height, in CSS pixels: "top,right,bottom,left,keyboard". */
        @JavascriptInterface
        public String getInsets() { return insets; }

        /** level: 0 normal, 1 high, 2 maximum. bt: use a Bluetooth headset microphone when one is connected. */
        @JavascriptInterface
        public void setMicPrefs(int level, boolean bt, boolean noisy) {
            micLevel = Math.max(0, Math.min(2, level));
            micNoisy = noisy;
            runOnUiThread(() -> { useBt = bt; if (!bt) btRouteOff(); });
        }

        /** What the last listening session used, for the status line: "bt|phone" + ",boost|plain". */
        @JavascriptInterface
        public String micInfo() { return (btIn != null ? "bt" : "phone") + "," + (usingBoost ? "boost" : (Build.VERSION.SDK_INT >= 33 && !boostFailed ? "ready" : "plain")); }

        @JavascriptInterface
        public void copyText(final String text) {
            runOnUiThread(() -> {
                android.content.ClipboardManager cm = (android.content.ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
                if (cm != null) cm.setPrimaryClip(android.content.ClipData.newPlainText("Quran", text));
            });
        }

        @JavascriptInterface
        public void setImmersive(final boolean on) {
            runOnUiThread(() -> {
                if (Build.VERSION.SDK_INT >= 30) {
                    WindowInsetsController c = getWindow().getInsetsController();
                    if (c == null) return;
                    int types = WindowInsets.Type.statusBars() | WindowInsets.Type.navigationBars();
                    if (on) {
                        c.setSystemBarsBehavior(WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
                        c.hide(types);
                    } else c.show(types);
                } else {
                    View dv = getWindow().getDecorView();
                    int keep = dv.getSystemUiVisibility() & View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
                    int f = BASE_UI | keep | (on ? (View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION) : 0);
                    dv.setSystemUiVisibility(f);
                }
            });
        }

        @JavascriptInterface
        public void setBarColor(final String hex, final boolean dark) {
            runOnUiThread(() -> {
                try {
                    int c = Color.parseColor(hex);
                    getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(c));
                    getWindow().getDecorView().setBackgroundColor(c);
                    getWindow().setStatusBarColor(c);
                    getWindow().setNavigationBarColor(c);
                    web.setBackgroundColor(c);
                    if (Build.VERSION.SDK_INT >= 30) {
                        WindowInsetsController ic = getWindow().getInsetsController();
                        if (ic != null) {
                            int mask = WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS;
                            ic.setSystemBarsAppearance(dark ? 0 : mask, mask);
                        }
                    } else if (Build.VERSION.SDK_INT >= 23) {
                        View d = getWindow().getDecorView();
                        int f = d.getSystemUiVisibility();
                        f = dark ? (f & ~View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR) : (f | View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR);
                        d.setSystemUiVisibility(f);
                    }
                } catch (Exception ignored) { }
            });
        }

        @JavascriptInterface
        public void keepScreenOn(final boolean on) {
            runOnUiThread(() -> {
                if (on) getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                else getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
            });
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] results) {
        if (requestCode != REQ_MIC) return;
        if (results.length > 0 && results[0] == PackageManager.PERMISSION_GRANTED && pendingLang != null) {
            startRecognizer(pendingLang);
        } else {
            emitError("not-allowed");
            emit("onend", null);
        }
        pendingLang = null;
    }

    private void startRecognizer(String lang) {
        if (!SpeechRecognizer.isRecognitionAvailable(this)) {
            emitError("service-not-allowed");
            emit("onend", null);
            return;
        }
        if (recognizer == null) {
            recognizer = SpeechRecognizer.createSpeechRecognizer(this);
            recognizer.setRecognitionListener(new Listener());
        }
        lastLang = lang;
        stopPump();
        if (btRouteOn()) { web.postDelayed(() -> { if (wantListen) startRecognizer(lang); }, 900); return; }   // give the headset time to connect
        Intent i = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE, lang);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, lang);
        i.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true);
        i.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1);
        i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 4000L);
        i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 3000L);
        i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 15000L);
        usingBoost = false;
        if (Build.VERSION.SDK_INT >= 33 && !boostFailed) {
            try {
                ParcelFileDescriptor rd = startPump();
                i.putExtra(RecognizerIntent.EXTRA_AUDIO_SOURCE, rd);
                i.putExtra(RecognizerIntent.EXTRA_AUDIO_SOURCE_CHANNEL_COUNT, 1);
                i.putExtra(RecognizerIntent.EXTRA_AUDIO_SOURCE_ENCODING, AudioFormat.ENCODING_PCM_16BIT);
                i.putExtra(RecognizerIntent.EXTRA_AUDIO_SOURCE_SAMPLING_RATE, PUMP_RATE);
                usingBoost = true;
                boostStart = SystemClock.elapsedRealtime();
            } catch (Exception e) {
                stopPump();
                usingBoost = false;
            }
        }
        try {
            recognizer.startListening(i);
        } catch (Exception e) {
            if (usingBoost) { boostFailed = true; stopPump(); startRecognizer(lang); return; }
            emitError("aborted");
            emit("onend", null);
        }
    }

    private static final int PUMP_RATE = 16000;

    /** Starts recording and returns the read end of a pipe carrying 16 kHz mono 16-bit PCM, with quiet speech raised. */
    private ParcelFileDescriptor startPump() throws Exception {
        int min = AudioRecord.getMinBufferSize(PUMP_RATE, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT);
        final boolean noisy = micNoisy;
        // In a noisy or windy place, VOICE_COMMUNICATION asks the phone for its call-quality processing
        // (on most phones this uses the second microphone to cancel surrounding noise).
        final AudioRecord rec = new AudioRecord(noisy ? MediaRecorder.AudioSource.VOICE_COMMUNICATION : MediaRecorder.AudioSource.VOICE_RECOGNITION, PUMP_RATE,
                AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, Math.max(min, PUMP_RATE));
        if (rec.getState() != AudioRecord.STATE_INITIALIZED) { rec.release(); throw new IllegalStateException("mic"); }
        if (btIn != null) { try { rec.setPreferredDevice(btIn); } catch (Exception ignored) { } }
        if (noisy) { try { if (NoiseSuppressor.isAvailable()) { NoiseSuppressor ns = NoiseSuppressor.create(rec.getAudioSessionId()); if (ns != null) ns.setEnabled(true); } } catch (Exception ignored) { } }
        try { if (AutomaticGainControl.isAvailable()) { AutomaticGainControl agc = AutomaticGainControl.create(rec.getAudioSessionId()); if (agc != null) agc.setEnabled(true); } } catch (Exception ignored) { }
        ParcelFileDescriptor[] p = ParcelFileDescriptor.createPipe();
        final OutputStream out = new ParcelFileDescriptor.AutoCloseOutputStream(p[1]);
        pumpRec = rec; pumpRead = p[0]; pumping = true; pumpPeakRms = 0;
        pumpThread = new Thread(() -> {
            short[] buf = new short[PUMP_RATE / 20];          // 50 ms
            byte[] bytes = new byte[buf.length * 2];
            float gain = 1f;
            // High-pass filter (2nd-order Butterworth): removes wind and traffic rumble below the voice.
            double fc = noisy ? 180.0 : 80.0, w0 = 2 * Math.PI * fc / PUMP_RATE, al = Math.sin(w0) / (2 * 0.7071), cs = Math.cos(w0), a0 = 1 + al;
            final float b0 = (float) ((1 + cs) / 2 / a0), b1 = (float) (-(1 + cs) / a0), b2 = b0, a1 = (float) (-2 * cs / a0), a2 = (float) ((1 - al) / a0);
            float x1 = 0, x2 = 0, y1 = 0, y2 = 0;
            try {
                rec.startRecording();
                while (pumping) {
                    int n = rec.read(buf, 0, buf.length);
                    if (n <= 0) continue;
                    for (int j = 0; j < n; j++) {
                        float x = buf[j], y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2;
                        x2 = x1; x1 = x; y2 = y1; y1 = y;
                        buf[j] = (short) Math.max(-32768, Math.min(32767, Math.round(y)));
                    }
                    double sum = 0; for (int j = 0; j < n; j++) sum += (double) buf[j] * buf[j];
                    float rms = (float) Math.sqrt(sum / n);
                    if (rms > pumpPeakRms) pumpPeakRms = rms;
                    // Raise quiet speech towards a normal speaking level (up to 3x, 6x or 12x by the sensitivity setting).
                    // Near-silence (room noise) is not raised further, so background hiss is not turned into "speech".
                    int lv = micLevel;
                    float gate = noisy ? GATE[lv] * 2f : GATE[lv], cap = noisy ? Math.min(MAX_GAIN[lv], 4f) : MAX_GAIN[lv];   // in noise, boost less
                    float want = rms > gate ? Math.max(1f, Math.min(cap, TARGET[lv] / rms)) : Math.min(gain, noisy ? 1f : 2f);
                    gain += (want - gain) * (want < gain ? 0.5f : 0.08f);   // come down fast, go up slowly
                    for (int j = 0; j < n; j++) {
                        float y = buf[j] * gain;
                        if (y > 24000f) y = 24000f + (y - 24000f) * 0.15f; else if (y < -24000f) y = -24000f + (y + 24000f) * 0.15f;  // soft limit
                        int v = Math.max(-32768, Math.min(32767, Math.round(y)));
                        bytes[2 * j] = (byte) (v & 0xff); bytes[2 * j + 1] = (byte) ((v >> 8) & 0xff);
                    }
                    out.write(bytes, 0, n * 2);
                }
            } catch (Exception ignored) {
                // the recognizer closed the stream: this listening session is over
            } finally {
                try { rec.stop(); } catch (Exception ignored) { }
                rec.release();
                try { out.close(); } catch (Exception ignored) { }
            }
        }, "mic-boost");
        pumpThread.start();
        return p[0];
    }

    private void stopPump() {
        pumping = false;
        if (pumpRead != null) { try { pumpRead.close(); } catch (Exception ignored) { } pumpRead = null; }
        pumpThread = null; pumpRec = null;
    }

    private class Listener implements RecognitionListener {
        private boolean ended;

        private void end() { stopPump(); if (!ended) { ended = true; emit("onend", null); } }

        private String first(Bundle b) {
            ArrayList<String> r = b == null ? null : b.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
            return (r == null || r.isEmpty()) ? "" : r.get(0);
        }

        private void result(String text, boolean fin) {
            try { JSONObject o = new JSONObject(); o.put("text", text); o.put("final", fin); emit("onresult", o); } catch (Exception ignored) { }
        }

        @Override public void onReadyForSpeech(Bundle params) { ended = false; emit("onstart", null); }
        @Override public void onBeginningOfSpeech() { }
        @Override public void onRmsChanged(float rmsdB) { }
        @Override public void onBufferReceived(byte[] buffer) { }
        @Override public void onEndOfSpeech() { }
        @Override public void onEvent(int eventType, Bundle params) { }

        @Override public void onPartialResults(Bundle b) {
            String t = first(b);
            if (!t.isEmpty()) result(t, false);
        }

        @Override public void onResults(Bundle b) {
            boostNoSpeech = 0;
            result(first(b), true);
            end();
        }

        @Override public void onError(int error) {
            if (usingBoost) {
                long t = SystemClock.elapsedRealtime() - boostStart;
                boolean refused = t < 3000 && error != SpeechRecognizer.ERROR_NO_MATCH && error != SpeechRecognizer.ERROR_SPEECH_TIMEOUT
                        && error != SpeechRecognizer.ERROR_NETWORK && error != SpeechRecognizer.ERROR_NETWORK_TIMEOUT
                        && error != SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS;
                boolean deaf = (error == SpeechRecognizer.ERROR_NO_MATCH || error == SpeechRecognizer.ERROR_SPEECH_TIMEOUT) && pumpPeakRms > 1500 && ++boostNoSpeech >= 2;
                if (refused || deaf) {   // this phone's recognizer will not take our stream: use its own microphone from now on
                    boostFailed = true; stopPump();
                    startRecognizer(lastLang);
                    return;
                }
            }
            String code;
            switch (error) {
                case SpeechRecognizer.ERROR_NO_MATCH:
                case SpeechRecognizer.ERROR_SPEECH_TIMEOUT: code = "no-speech"; break;
                case SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS: code = "not-allowed"; break;
                case SpeechRecognizer.ERROR_NETWORK:
                case SpeechRecognizer.ERROR_NETWORK_TIMEOUT:
                case SpeechRecognizer.ERROR_SERVER: code = "network"; break;
                case SpeechRecognizer.ERROR_AUDIO: code = "audio-capture"; break;
                default: code = "aborted";
            }
            emitError(code);
            end();
        }
    }

    /* ---------------- Lifecycle ---------------- */

    @Override
    public void onBackPressed() {
        web.evaluateJavascript("window.__back ? window.__back() : false", value -> {
            if (!"true".equals(value)) {
                if (web.canGoBack()) web.goBack(); else MainActivity.super.onBackPressed();
            }
        });
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (recognizer != null) recognizer.cancel();
        stopPump();
        btRouteOff();
        web.evaluateJavascript("window.__pause && window.__pause()", null);
    }

    @Override
    protected void onDestroy() {
        if (recognizer != null) { recognizer.destroy(); recognizer = null; }
        stopPump();
        btRouteOff();
        web.destroy();
        super.onDestroy();
    }
}
