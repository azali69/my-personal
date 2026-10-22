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
import android.media.MediaMetadata;
import android.media.session.MediaSession;
import android.media.session.PlaybackState;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.media.audiofx.AutomaticGainControl;
import android.media.audiofx.NoiseSuppressor;
import android.os.ParcelFileDescriptor;
import android.os.SystemClock;
import android.view.ActionMode;
import android.view.Menu;
import android.view.MenuItem;
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
import android.content.Context;
import android.hardware.GeomagneticField;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.PowerManager;
import android.provider.Settings;

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

    /* Reciter player: registered with Android as a media player, so headset / Bluetooth / lock-screen buttons control it,
       the lock screen shows what is playing. */
    private MediaSession msess;
    /* Audio focus is left to the WebView itself (it already takes focus when the reciter plays and pauses when another app
       or a call takes the audio). Asking for focus here as well made the app fight its own WebView and silenced playback. */
    private void mediaCmd(String c) { runOnUiThread(() -> web.evaluateJavascript("window.__media && window.__media('" + c + "')", null)); }

    private void ensureSession() {
        PlaybackService.onPauseCmd = () -> mediaCmd("pause"); PlaybackService.onPlayCmd = () -> mediaCmd("play");
        PlaybackService.onNextCmd = () -> mediaCmd("next"); PlaybackService.onStopCmd = () -> mediaCmd("stop");
        if (msess != null) return;
        msess = new MediaSession(this, "MyPersonalQuran");
        msess.setCallback(new MediaSession.Callback() {
            @Override public void onPlay() { mediaCmd("play"); }
            @Override public void onPause() { mediaCmd("pause"); }
            @Override public void onSkipToNext() { mediaCmd("next"); }
            @Override public void onSkipToPrevious() { mediaCmd("prev"); }
            @Override public void onStop() { mediaCmd("stop"); }
        });
    }
    private volatile String insets = "";
    private static final int BASE_UI = View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION;
    private SpeechRecognizer recognizer;
    private String pendingLang;
    /* Voice search: short listening, several languages allowed (first is the main one). */
    private boolean searchMode = false, searchPlain = false;
    private long searchStart = 0;
    /* Voice search keeps the spoken audio, so it can be recognised again in another language ("Auto"). */
    private final java.io.ByteArrayOutputStream searchBuf = new java.io.ByteArrayOutputStream();
    private ParcelFileDescriptor replayFd = null;
    private String[] searchLangs = new String[0];

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

    /* Recording the person's own recitation (Hafazan), saved as WAV in the app's private storage and served to the page at /rec/. */
    private final Object recLock = new Object();
    private java.io.RandomAccessFile recOut;
    private File recFile;
    private long recBytes = 0;
    private volatile boolean recActive = false, recStandalone = false;
    private Thread recThread;
    private static final int REC_KEEP = 30;

    private File recDir() { File d = new File(getFilesDir(), "rec"); if (!d.exists()) d.mkdirs(); return d; }

    /** Adds 16 kHz mono 16-bit PCM to the open recording. */
    private void recWrite(byte[] b, int len) {
        synchronized (recLock) {
            if (!recActive || recOut == null) return;
            try { recOut.write(b, 0, len); recBytes += len; } catch (Exception ignored) { }
        }
    }

    private static void wavHeader(java.io.RandomAccessFile f, long data) throws Exception {
        f.seek(0);
        java.nio.ByteBuffer h = java.nio.ByteBuffer.allocate(44).order(java.nio.ByteOrder.LITTLE_ENDIAN);
        h.put("RIFF".getBytes()).putInt((int) (36 + data)).put("WAVE".getBytes()).put("fmt ".getBytes()).putInt(16)
         .putShort((short) 1).putShort((short) 1).putInt(PUMP_RATE).putInt(PUMP_RATE * 2).putShort((short) 2).putShort((short) 16)
         .put("data".getBytes()).putInt((int) data);
        f.write(h.array());
    }

    /** When the speech recognizer uses its own microphone (no boost), record with a separate recorder. Some phones give it silence. */
    private void recStandaloneStart() {
        if (recThread != null) return;
        recStandalone = true;
        recThread = new Thread(() -> {
            AudioRecord r = null;
            try {
                int min = AudioRecord.getMinBufferSize(PUMP_RATE, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT);
                r = new AudioRecord(MediaRecorder.AudioSource.MIC, PUMP_RATE, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, Math.max(min, PUMP_RATE));
                if (btIn != null) { try { r.setPreferredDevice(btIn); } catch (Exception ignored) { } }
                r.startRecording();
                byte[] b = new byte[PUMP_RATE / 10];
                while (recStandalone && recActive) { int n = r.read(b, 0, b.length); if (n > 0) recWrite(b, n); }
            } catch (Exception ignored) {
            } finally { if (r != null) { try { r.stop(); } catch (Exception ignored) { } r.release(); } }
        }, "rec-standalone");
        recThread.start();
    }

    private void recStandaloneStop() { recStandalone = false; recThread = null; }

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
        // the BOOX pen SDK calls hidden Android methods (as in My Personal eReader)
        if (isOnyx() && Build.VERSION.SDK_INT >= 30) { try { org.lsposed.hiddenapibypass.HiddenApiBypass.addHiddenApiExemptions(""); } catch (Throwable ignored) { } }
        // Android may rebuild the screen after a file picker (backup, sync) or from Recents: it then hands back the intent the app
        // was first opened with, so an old share would open Scan & check again. Only a fresh launch takes the share and the "open" target.
        boolean fresh = savedInstanceState == null && (getIntent() == null || (getIntent().getFlags() & Intent.FLAG_ACTIVITY_LAUNCHED_FROM_HISTORY) == 0);
        openTarget = fresh && getIntent() != null ? getIntent().getStringExtra("open") : null;
        if (fresh) takeShare(getIntent());
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
            int t, r, b, l, k, ct = 0, cb = 0;   // ct/cb: the camera cut-out only (the page may use the space of hidden bars)
            if (Build.VERSION.SDK_INT >= 30) {
                android.graphics.Insets i = ins.getInsetsIgnoringVisibility(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                t = i.top; r = i.right; b = i.bottom; l = i.left;
                android.graphics.Insets cu = ins.getInsetsIgnoringVisibility(WindowInsets.Type.displayCutout());
                ct = cu.top; cb = cu.bottom;
                k = ins.getInsets(WindowInsets.Type.ime()).bottom;   // the on-screen keyboard (0 when hidden)
            } else {
                k = Math.max(0, ins.getSystemWindowInsetBottom() - ins.getStableInsetBottom());
                t = ins.getStableInsetTop(); r = ins.getStableInsetRight(); b = ins.getStableInsetBottom(); l = ins.getStableInsetLeft();
                if (Build.VERSION.SDK_INT >= 28 && ins.getDisplayCutout() != null) {
                    android.view.DisplayCutout c = ins.getDisplayCutout();
                    t = Math.max(t, c.getSafeInsetTop()); r = Math.max(r, c.getSafeInsetRight());
                    b = Math.max(b, c.getSafeInsetBottom()); l = Math.max(l, c.getSafeInsetLeft());
                    ct = c.getSafeInsetTop(); cb = c.getSafeInsetBottom();
                }
            }
            String now = Math.round(t / d) + "," + Math.round(r / d) + "," + Math.round(b / d) + "," + Math.round(l / d) + "," + Math.round(k / d) + "," + Math.round(ct / d) + "," + Math.round(cb / d);
            if (!now.equals(insets)) { insets = now; web.evaluateJavascript("window.__insets && window.__insets()", null); }
            return ins;
        });

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(false);   // the reciter player moves to the next ayah by itself
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        // The app has its own text-size setting: ignore the phone's system font size so pages look the same on every phone
        s.setTextZoom(100);

        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
                .setDomain(HOST)
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .addPathHandler("/rec/", new WebViewAssetLoader.InternalStoragePathHandler(this, recDir()))
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
        web.addJavascriptInterface(new ExtraBridge(), "AndroidExtra");
        try { PrayerAlarms.schedule(this); } catch (Exception ignored) { }
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
                searchMode = false;
                if (Build.VERSION.SDK_INT >= 23 &&
                        checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                    pendingLang = lang;
                    requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, REQ_MIC);
                    return;
                }
                startRecognizer(lang);
            });
        }

        /** Voice search: langs is a comma list such as "ar-SA,ms-MY,en-US"; the first is the main language. */
        @JavascriptInterface
        public void startSearch(final String langs) {
            runOnUiThread(() -> {
                searchLangs = langs.split(",");
                searchMode = true;
                synchronized (searchBuf) { searchBuf.reset(); }
                wantListen = true;
                if (Build.VERSION.SDK_INT >= 23 &&
                        checkSelfPermission(Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                    pendingLang = searchLangs[0];
                    requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO}, REQ_MIC);
                    return;
                }
                startRecognizer(searchLangs[0]);
            });
        }

        /** Recognise the last voice-search audio again, in another language. False if this phone cannot (needs Android 13+ and the boost path). */
        @JavascriptInterface
        public boolean searchReplay(final String lang) {
            final byte[] audio; synchronized (searchBuf) { audio = searchBuf.toByteArray(); }
            if (Build.VERSION.SDK_INT < 33 || boostFailed || audio.length < PUMP_RATE / 2) return false;
            try {
                ParcelFileDescriptor[] p = ParcelFileDescriptor.createPipe();
                final OutputStream out = new ParcelFileDescriptor.AutoCloseOutputStream(p[1]);
                new Thread(() -> { try { out.write(audio); } catch (Exception ignored) { } finally { try { out.close(); } catch (Exception ignored) { } } }, "search-replay").start();
                runOnUiThread(() -> { searchMode = true; searchPlain = true; wantListen = true; searchLangs = new String[]{lang}; replayFd = p[0]; startRecognizer(lang); });
                return true;
            } catch (Exception e) { return false; }
        }

        @JavascriptInterface
        public void stop() {
            runOnUiThread(() -> { wantListen = false; if (recognizer != null) recognizer.stopListening(); stopPump(); btRouteOff(); });
        }

        /** Fixed margins for the status bar, navigation bar and camera cutout, plus the keyboard height, in CSS pixels: "top,right,bottom,left,keyboard". */
        @JavascriptInterface
        public String getInsets() { return insets; }

        /** Starts saving the recitation to a new WAV file. */
        @JavascriptInterface
        public boolean recStart() {
            synchronized (recLock) {
                try {
                    recFile = new File(recDir(), "rec-" + System.currentTimeMillis() + ".wav");
                    recOut = new java.io.RandomAccessFile(recFile, "rw");
                    wavHeader(recOut, 0); recBytes = 0; recActive = true;
                } catch (Exception e) { recActive = false; return false; }
            }
            return true;
        }

        /** Finishes the recording. Returns "name,seconds", or "" if nothing was recorded. Keeps the newest recordings only. */
        @JavascriptInterface
        public String recStop() {
            String res = "";
            recStandaloneStop();
            synchronized (recLock) {
                recActive = false;
                try {
                    if (recOut != null) { wavHeader(recOut, recBytes); recOut.close(); }
                    if (recFile != null) {
                        if (recBytes < PUMP_RATE) recFile.delete();   // under half a second: nothing worth keeping
                        else res = recFile.getName() + "," + (recBytes / (PUMP_RATE * 2));
                    }
                } catch (Exception ignored) { }
                recOut = null; recFile = null;
            }
            File[] all = recDir().listFiles();
            if (all != null && all.length > REC_KEEP) {
                java.util.Arrays.sort(all, (a, b) -> Long.compare(a.lastModified(), b.lastModified()));
                for (int k = 0; k < all.length - REC_KEEP; k++) all[k].delete();
            }
            return res;
        }

        /** Whether a recording file still exists (old ones are removed). */
        @JavascriptInterface
        public boolean recExists(String name) { return name != null && !name.contains("/") && new File(recDir(), name).exists(); }

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

        /** The page tells Android what the reciter player is doing: state is "playing", "paused" or "stopped". */
        @JavascriptInterface
        public void mediaState(final String state, final String title, final String subtitle) {
            runOnUiThread(() -> {
                ensureSession();
                long actions = PlaybackState.ACTION_PLAY | PlaybackState.ACTION_PAUSE | PlaybackState.ACTION_PLAY_PAUSE
                        | PlaybackState.ACTION_SKIP_TO_NEXT | PlaybackState.ACTION_SKIP_TO_PREVIOUS | PlaybackState.ACTION_STOP;
                if ("stopped".equals(state)) {
                    msess.setPlaybackState(new PlaybackState.Builder().setActions(actions).setState(PlaybackState.STATE_STOPPED, 0, 0).build());
                    msess.setActive(false);
                    PlaybackService.hide();
                    return;
                }
                msess.setMetadata(new MediaMetadata.Builder()
                        .putString(MediaMetadata.METADATA_KEY_TITLE, title == null ? "" : title)
                        .putString(MediaMetadata.METADATA_KEY_ARTIST, subtitle == null ? "" : subtitle)
                        .putString(MediaMetadata.METADATA_KEY_ALBUM, "My Personal Quran").build());
                msess.setPlaybackState(new PlaybackState.Builder().setActions(actions)
                        .setState("playing".equals(state) ? PlaybackState.STATE_PLAYING : PlaybackState.STATE_PAUSED, PlaybackState.PLAYBACK_POSITION_UNKNOWN, 1f).build());
                msess.setActive(true);
                // keep playing with the screen off: a foreground "now playing" service (see PlaybackService)
                PlaybackService.token = msess.getSessionToken();
                PlaybackService.show(MainActivity.this, title, subtitle, "playing".equals(state));
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
        if (requestCode == REQ_LOC) { boolean ok = results.length > 0 && results[0] == PackageManager.PERMISSION_GRANTED; if (ok) findLocation(); else js("window.__loc && window.__loc({error:'denied'})"); return; }
        if (requestCode == REQ_NOTIF) { js("window.__notifPerm && window.__notifPerm()"); return; }
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
        if (searchMode) {
            searchStart = SystemClock.elapsedRealtime();
            // a short query: stop soon after the person stops speaking
            i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 1500L);
            i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 1200L);
            if (searchLangs.length > 1) {
                String[] more = java.util.Arrays.copyOfRange(searchLangs, 1, searchLangs.length);
                i.putExtra("android.speech.extra.EXTRA_ADDITIONAL_LANGUAGES", more);   // Google's recognizer: also accept these
                ArrayList<String> all = new ArrayList<>(java.util.Arrays.asList(searchLangs));
                if (Build.VERSION.SDK_INT >= 33 && !searchPlain) {
                    i.putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_DETECTION, true);
                    i.putStringArrayListExtra(RecognizerIntent.EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES, all);
                }
                if (Build.VERSION.SDK_INT >= 34 && !searchPlain) {
                    i.putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_SWITCH, RecognizerIntent.LANGUAGE_SWITCH_BALANCED);
                    i.putStringArrayListExtra(RecognizerIntent.EXTRA_LANGUAGE_SWITCH_ALLOWED_LANGUAGES, all);
                }
            }
        } else {
            i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 4000L);
            i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 3000L);
            i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 15000L);
        }
        usingBoost = false;
        if (replayFd != null) {
            i.putExtra(RecognizerIntent.EXTRA_AUDIO_SOURCE, replayFd);
            i.putExtra(RecognizerIntent.EXTRA_AUDIO_SOURCE_CHANNEL_COUNT, 1);
            i.putExtra(RecognizerIntent.EXTRA_AUDIO_SOURCE_ENCODING, AudioFormat.ENCODING_PCM_16BIT);
            i.putExtra(RecognizerIntent.EXTRA_AUDIO_SOURCE_SAMPLING_RATE, PUMP_RATE);
            replayFd = null;
        } else if (Build.VERSION.SDK_INT >= 33 && !boostFailed) {
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
        if (recActive) { if (usingBoost) recStandaloneStop(); else recStandaloneStart(); }
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
                    recWrite(bytes, n * 2);
                    if (searchMode) synchronized (searchBuf) { if (searchBuf.size() < PUMP_RATE * 2 * 20) searchBuf.write(bytes, 0, n * 2); }
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
            // A recognizer that refuses the language-detection request: ask again without it.
            if (searchMode && !searchPlain && SystemClock.elapsedRealtime() - searchStart < 2500
                    && (error == SpeechRecognizer.ERROR_CLIENT || error == 12 || error == 13)) {
                searchPlain = true;
                startRecognizer(searchLangs[0]);
                return;
            }
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


    /* ---------------- Prayer alerts, adhan files, location, compass ---------------- */
    private static final int REQ_NOTIF = 21, REQ_LOC = 22, REQ_PICK = 23, REQ_SAVE = 24, REQ_OPEN = 25, REQ_SYNC = 28, REQ_GAUTH = 29;   // 26/27 are the camera and image scans
    private String pendingBackup = null, openedBackup = null;   // backup file text: to be written / just read
    private String pickSlot = null;
    private SensorManager sm; private SensorEventListener compassL; private float decl = 0f; private long lastCompass = 0;

    private static String readAll(InputStream in) throws java.io.IOException {
        try (InputStream i = in) { java.io.ByteArrayOutputStream bo = new java.io.ByteArrayOutputStream(); byte[] b = new byte[16384]; int n; while ((n = i.read(b)) > 0) bo.write(b, 0, n); return new String(bo.toByteArray(), java.nio.charset.StandardCharsets.UTF_8); } }
    private void js(final String code) { runOnUiThread(() -> web.evaluateJavascript(code, null)); }

    /* Opened from a prayer notification: the page goes straight to the prayer times. */
    private volatile String openTarget = null;
    @Override protected void onNewIntent(Intent i) {
        super.onNewIntent(i); setIntent(i);
        String o = i == null ? null : i.getStringExtra("open");
        if (o != null && web != null) { final String w = o.replaceAll("[^a-z]", ""); js("window.__openFrom && window.__openFrom('" + w + "')"); }
        if (takeShare(i) && web != null) js("window.__sharedIn && window.__sharedIn()");
    }

    /* ---------------- Scan & check: camera, picture, "Share to" this app ---------------- */
    private static final int REQ_CAM = 26, REQ_IMG = 27;
    private volatile String sharedText = null; private volatile Uri sharedImage = null; private volatile boolean sharedImageNew = false;
    private Uri camUri = null; private String scanLang = "ms";

    /** Keeps what another app shared: text as it is; a picture copied into the cache (the read grant does not last). */
    private boolean takeShare(Intent i) {
        if (i == null || !Intent.ACTION_SEND.equals(i.getAction())) return false;
        String type = i.getType() == null ? "" : i.getType();
        if (type.startsWith("text/")) {
            CharSequence t = i.getCharSequenceExtra(Intent.EXTRA_TEXT);
            if (t == null) return false;
            sharedText = t.toString(); i.setAction(Intent.ACTION_MAIN); return true;
        }
        if (type.startsWith("image/")) {
            Uri u = i.getParcelableExtra(Intent.EXTRA_STREAM);
            if (u == null) return false;
            try {
                File dir = new File(getCacheDir(), "scan"); dir.mkdirs();
                File f = new File(dir, "shared.img");
                try (InputStream in = getContentResolver().openInputStream(u); OutputStream out = new FileOutputStream(f)) {
                    byte[] b = new byte[65536]; int n; long total = 0;
                    while ((n = in.read(b)) > 0) { out.write(b, 0, n); total += n; if (total > 40_000_000) throw new Exception("too big"); }
                }
                sharedImage = Uri.fromFile(f); sharedImageNew = true; i.setAction(Intent.ACTION_MAIN); return true;
            } catch (Exception e) { return false; }
        }
        return false;
    }
    private File lastScan = null;   // the last picture read, kept so it can be sent to Google Lens
    private void runScan(Uri u, String lang) {
        if (u == null) { js("window.__scanned && window.__scanned({cancel:1})"); return; }
        js("window.__scanBusy && window.__scanBusy()");
        final Uri src = u;
        new Thread(() -> {
            Uri use = src;
            try {
                File dir = new File(getCacheDir(), "scan"); dir.mkdirs(); File f = new File(dir, "last.img");
                try (InputStream in = getContentResolver().openInputStream(src); OutputStream out = new FileOutputStream(f)) {
                    byte[] b = new byte[65536]; int n; while ((n = in.read(b)) > 0) out.write(b, 0, n); }
                lastScan = f; use = Uri.fromFile(f);
            } catch (Exception ignored) { }
            ScanOcr.run(this, use, lang, json -> js("window.__scanned && window.__scanned(" + json + ")"));
        }, "scan-copy").start();
    }
    /** Google Lens reads Arabic very well: send it the last picture, or open its camera. The text is then shared back. */
    private boolean tryStart(Intent i) { try { startActivity(i); return true; } catch (Exception e) { return false; } }
    private void openLens() {
        if (lastScan != null && lastScan.exists()) {
            Uri u = androidx.core.content.FileProvider.getUriForFile(this, getPackageName() + ".files", lastScan);
            Intent send = new Intent(Intent.ACTION_SEND).setType("image/jpeg").putExtra(Intent.EXTRA_STREAM, u).addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            if (tryStart(new Intent(send).setClassName("com.google.android.googlequicksearchbox", "com.google.android.apps.search.lens.LensShareEntryPointActivity"))) return;
            if (tryStart(new Intent(send).setPackage("com.google.ar.lens"))) return;
            if (tryStart(Intent.createChooser(send, "Read the text with…"))) return;
        }
        if (tryStart(new Intent(Intent.ACTION_VIEW, Uri.parse("googleapp://lens")))) return;
        Intent l = getPackageManager().getLaunchIntentForPackage("com.google.ar.lens");
        if (l != null && tryStart(l)) return;
        js("window.__scanned && window.__scanned(" + ScanOcr.err("Google Lens is not on this phone. Install the Google app or Google Lens from the Play Store.") + ")");
    }
    private class ExtraBridge {
        @JavascriptInterface public void lens() { runOnUiThread(MainActivity.this::openLens); }
        @JavascriptInterface public String ocrReady() { return ArabicOcr.ready(MainActivity.this) ? "1" : "0"; }
        @JavascriptInterface public void ocrDownload() {
            new Thread(() -> {
                boolean ok = false;
                try { ArabicOcr.download(MainActivity.this, pct -> js("window.__ocrProg && window.__ocrProg(" + pct + ")")); ok = ArabicOcr.ready(MainActivity.this); }
                catch (Exception e) { ok = false; }
                final boolean r = ok; js("window.__ocrDone && window.__ocrDone(" + r + ")");
            }, "ocr-download").start();
        }
        @JavascriptInterface public String takeShared() {
            try {
                JSONObject o = new JSONObject();
                String t = sharedText; sharedText = null;
                if (t != null) o.put("text", t);
                if (sharedImageNew) { sharedImageNew = false; o.put("image", true); }
                return o.length() == 0 ? "" : o.toString();
            } catch (Exception e) { return ""; }
        }
        @JavascriptInterface public void scanShared(String lang) { final String l = lang; final Uri u = sharedImage; runOnUiThread(() -> runScan(u, l)); }
        @JavascriptInterface public void scanCamera(String lang) {
            scanLang = lang;
            runOnUiThread(() -> {
                try {
                    File dir = new File(getCacheDir(), "scan"); dir.mkdirs();
                    File f = new File(dir, "camera.jpg"); if (f.exists()) f.delete();
                    camUri = androidx.core.content.FileProvider.getUriForFile(MainActivity.this, getPackageName() + ".files", f);
                    Intent it = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE).putExtra(android.provider.MediaStore.EXTRA_OUTPUT, camUri)
                        .addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    startActivityForResult(it, REQ_CAM);
                } catch (Exception e) { js("window.__scanned && window.__scanned(" + ScanOcr.err("No camera app could be opened.") + ")"); }
            });
        }
        @JavascriptInterface public void scanPicture(String lang) {
            scanLang = lang;
            runOnUiThread(() -> {
                try { startActivityForResult(new Intent(Intent.ACTION_GET_CONTENT).addCategory(Intent.CATEGORY_OPENABLE).setType("image/*"), REQ_IMG); }
                catch (Exception e) { js("window.__scanned && window.__scanned(" + ScanOcr.err("No picture app could be opened.") + ")"); }
            });
        }
        @JavascriptInterface public String takeOpen() { String o = openTarget; openTarget = null; return o == null ? "" : o; }
        @JavascriptInterface public void setPrayerStatus(String json, String mode) { PrayerStatus.save(MainActivity.this, json, mode); }
        @JavascriptInterface public void setPrayerAlarms(String json) { PrayerAlarms.save(MainActivity.this, json); }
        @JavascriptInterface public String alarmStatus() {
            try {
                JSONObject o = new JSONObject();
                o.put("notif", Build.VERSION.SDK_INT < 33 || checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED);
                o.put("exact", PrayerAlarms.canExact(MainActivity.this));
                PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
                o.put("battery", pm != null && pm.isIgnoringBatteryOptimizations(getPackageName()));
                File a = AdhanService.adhanFile(MainActivity.this, "makkah"), b = AdhanService.adhanFile(MainActivity.this, "madinah");
                o.put("makkah", a == null ? "" : PrayerAlarms.prefs(MainActivity.this).getString("name_makkah", a.getName()));
                o.put("madinah", b == null ? "" : PrayerAlarms.prefs(MainActivity.this).getString("name_madinah", b.getName()));
                File t = AdhanService.adhanFile(MainActivity.this, "mytone");
                o.put("mytone", t == null ? "" : PrayerAlarms.prefs(MainActivity.this).getString("name_mytone", t.getName()));
                o.put("next", PrayerAlarms.prefs(MainActivity.this).getString("pending", ""));
                return o.toString();
            } catch (Exception e) { return "{}"; }
        }
        @JavascriptInterface public void askNotifications() { if (Build.VERSION.SDK_INT >= 33) runOnUiThread(() -> requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, REQ_NOTIF)); }
        @JavascriptInterface public void openExactAlarm() {
            runOnUiThread(() -> { try { if (Build.VERSION.SDK_INT >= 31) startActivity(new Intent(Settings.ACTION_REQUEST_SCHEDULE_EXACT_ALARM, Uri.parse("package:" + getPackageName()))); } catch (Exception e) { openAppSettings(); } }); }
        @JavascriptInterface public void openBattery() {
            runOnUiThread(() -> { try { startActivity(new Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, Uri.parse("package:" + getPackageName()))); } catch (Exception e) { openAppSettings(); } }); }
        @JavascriptInterface public void openNotifSettings() {
            runOnUiThread(() -> { try { startActivity(new Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS).putExtra(Settings.EXTRA_APP_PACKAGE, getPackageName())); } catch (Exception e) { openAppSettings(); } }); }
        @JavascriptInterface public void pickAdhan(String slot) {
            if (!"makkah".equals(slot) && !"madinah".equals(slot) && !"mytone".equals(slot)) return;
            pickSlot = slot;
            runOnUiThread(() -> { try { startActivityForResult(new Intent(Intent.ACTION_OPEN_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("audio/*"), REQ_PICK); } catch (Exception e) { js("window.__adhanPicked && window.__adhanPicked('" + slot + "','')"); } }); }
        /* Backup of the app's settings, bookmarks and notes: the person chooses where the file goes and where it comes from. */
        @JavascriptInterface public void saveBackup(String name, String json) { pendingBackup = json;
            // kept on disk too: if Android rebuilds the screen while the file picker is open, the field is lost
            try (OutputStream o = new FileOutputStream(new File(getCacheDir(), "pending-backup.json"))) { o.write(json.getBytes(java.nio.charset.StandardCharsets.UTF_8)); } catch (Exception ignored) { }
            runOnUiThread(() -> { try { startActivityForResult(new Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("application/json").putExtra(Intent.EXTRA_TITLE, name), REQ_SAVE); }
                catch (Exception e) { pendingBackup = null; js("window.__backupSaved && window.__backupSaved(false)"); } }); }
        @JavascriptInterface public void openBackup() {
            runOnUiThread(() -> { try { startActivityForResult(new Intent(Intent.ACTION_OPEN_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("*/*"), REQ_OPEN); }
                catch (Exception e) { js("window.__backupOpened && window.__backupOpened(false)"); } }); }
        /* Sync between the person's phones and tablets (Azli, 17 Oct 2026): one file they choose in Google Drive (or any
           cloud folder), kept by Android's document permission; the app reads and writes it, Drive keeps it the same everywhere. */
        /* Google Drive sync (Azli, 20 Oct 2026): sign in with Google and keep one file in the app's hidden Drive folder
           (scope drive.appdata: the app sees only its own folder, nothing else in Drive). The OAuth client is the Android
           client 787421539161-pskuco9b997q2tri0g6ndcujfudm990l, matched by package name and signing SHA-1. */
        @JavascriptInterface public void gSignIn() {
            runOnUiThread(() -> { try {
                com.google.android.gms.auth.api.identity.Identity.getAuthorizationClient(MainActivity.this).authorize(gReq())
                  .addOnSuccessListener(r -> { if (r.hasResolution() && r.getPendingIntent() != null) {
                        try { startIntentSenderForResult(r.getPendingIntent().getIntentSender(), REQ_GAUTH, null, 0, 0, 0); } catch (Exception e) { js("window.__gSigned && window.__gSigned('')"); } }
                      else gAfterAuth(r.getAccessToken()); })
                  .addOnFailureListener(e -> js("window.__gSigned && window.__gSigned('!'+" + JSONObject.quote(String.valueOf(e.getMessage())) + ")"));
            } catch (Exception e) { js("window.__gSigned && window.__gSigned('!'+" + JSONObject.quote(String.valueOf(e.getMessage())) + ")"); } }); }
        /* Sync reads and writes go over the network (Drive) or through the cloud app, which can take seconds: run them on a
           background thread and answer through window.__syncDone(id, result), so the page never waits (Azli, 21 Oct 2026: touch lagged). */
        @JavascriptInterface public void syncReadAsync(final String id) {
            new Thread(() -> { String r; try { r = syncRead(); } catch (Exception e) { r = "!" + e.getMessage(); }
                js("window.__syncDone && window.__syncDone(" + JSONObject.quote(id) + "," + JSONObject.quote(r) + ")"); }).start(); }
        @JavascriptInterface public void syncWriteAsync(final String id, final String text) {
            new Thread(() -> { boolean ok; try { ok = syncWrite(text); } catch (Exception e) { ok = false; }
                js("window.__syncDone && window.__syncDone(" + JSONObject.quote(id) + "," + (ok ? "'1'" : "''") + ")"); }).start(); }
        /* BOOX fast pen for the Notepad (Azli, 22 Oct 2026; the same Onyx pen SDK as My Personal eReader): the e-ink screen shows the
           stroke at once, as in BOOX Notes, and the finished stroke goes to the page (window.__boox). Area in fractions of the screen. */
        @JavascriptInterface public boolean booxAvailable() { return isOnyx(); }
        @JavascriptInterface public void booxStart(final double l, final double t, final double r, final double b, final double cssW, final double width, final String color) {
            runOnUiThread(() -> { try {
                int vw = web.getWidth(), vh = web.getHeight(); bxDensity = vw / (float) Math.max(1d, cssW);
                android.graphics.Rect lim = new android.graphics.Rect((int) Math.round(l * vw), (int) Math.round(t * vh), (int) Math.round(r * vw), (int) Math.round(b * vh));
                if (bxHelper == null) bxHelper = com.onyx.android.sdk.pen.TouchHelper.create(web, bxCb);
                bxHelper.setStrokeWidth(Math.max(1f, (float) width * bxDensity));
                bxHelper.setLimitRect(lim, new java.util.ArrayList<android.graphics.Rect>());
                if (!bxOpened) { bxHelper.openRawDrawing(); bxOpened = true; }
                bxHelper.setStrokeStyle(com.onyx.android.sdk.pen.TouchHelper.STROKE_STYLE_PENCIL);
                try { bxHelper.setStrokeColor(Color.parseColor(color)); } catch (Throwable ignored) { }
                bxHelper.setRawDrawingEnabled(true);
                try { bxHelper.setRawInputReaderEnable(true); } catch (Throwable ignored) { }
                try { bxHelper.forceSetRawDrawingEnabled(true); } catch (Throwable ignored) { }
                js("window.__booxOk && window.__booxOk(1," + vw + ")");
            } catch (Throwable e) { js("window.__booxOk && window.__booxOk(0," + JSONObject.quote(String.valueOf(e)) + ")"); } }); }
        @JavascriptInterface public void booxEnable(final boolean on) {
            runOnUiThread(() -> { try { if (bxHelper != null && bxOpened) { bxHelper.setRawDrawingEnabled(on); try { bxHelper.setRawInputReaderEnable(on); } catch (Throwable ignored) { }
                if (on) { try { bxHelper.forceSetRawDrawingEnabled(true); } catch (Throwable ignored) { } } } } catch (Throwable ignored) { } }); }
        @JavascriptInterface public void booxStop() {
            runOnUiThread(() -> { try { if (bxHelper != null && bxOpened) { bxHelper.setRawDrawingEnabled(false); bxHelper.closeRawDrawing(); } } catch (Throwable ignored) { } bxOpened = false; }); }
        @JavascriptInterface public String gAccount() { return PrayerAlarms.prefs(MainActivity.this).getString("gsync", ""); }
        @JavascriptInterface public void syncPick(boolean create) {
            runOnUiThread(() -> { try {
                Intent i = create ? new Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("application/json").putExtra(Intent.EXTRA_TITLE, "MyPersonalQuran-sync.json")
                                  : new Intent(Intent.ACTION_OPEN_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType("*/*");
                i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION | Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION);
                startActivityForResult(i, REQ_SYNC); } catch (Exception e) { js("window.__syncPicked && window.__syncPicked('')"); } }); }
        @JavascriptInterface public String syncName() { String g = gAccount(); return g.isEmpty() ? PrayerAlarms.prefs(MainActivity.this).getString("syncName", "") : "Google Drive (" + g + ")"; }
        @JavascriptInterface public void syncOff() {
            String u = PrayerAlarms.prefs(MainActivity.this).getString("syncUri", "");
            try { if (!u.isEmpty()) getContentResolver().releasePersistableUriPermission(Uri.parse(u), Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION); } catch (Exception ignored) { }
            PrayerAlarms.prefs(MainActivity.this).edit().remove("syncUri").remove("syncName").remove("gsync").remove("gfile").apply(); }
        /** The sync file's text, "" if empty, or "!error" when it cannot be read. */
        @JavascriptInterface public String syncRead() {
            if (!gAccount().isEmpty()) return gRead();
            String u = PrayerAlarms.prefs(MainActivity.this).getString("syncUri", ""); if (u.isEmpty()) return "!none";
            // ask the cloud app (Google Drive, OneDrive) for its newest copy first, so a change from the other device is seen
            try { if (Build.VERSION.SDK_INT >= 26) getContentResolver().refresh(Uri.parse(u), null, null); } catch (Exception ignored) { }
            try (InputStream in = getContentResolver().openInputStream(Uri.parse(u))) {
                java.io.ByteArrayOutputStream bo = new java.io.ByteArrayOutputStream(); byte[] b = new byte[16384]; int n; long total = 0;
                while ((n = in.read(b)) > 0) { bo.write(b, 0, n); total += n; if (total > 20_000_000) return "!too big"; }
                return new String(bo.toByteArray(), java.nio.charset.StandardCharsets.UTF_8);
            } catch (Exception e) { return "!" + e.getClass().getSimpleName(); } }
        /** Writes the sync file. Cloud apps differ in the write modes they accept (Google Drive refuses "wt" on some phones), so "wt", "w" and "rwt" are tried in turn. */
        @JavascriptInterface public boolean syncWrite(String text) {
            if (!gAccount().isEmpty()) return gWrite(text);
            String u = PrayerAlarms.prefs(MainActivity.this).getString("syncUri", ""); if (u.isEmpty()) return false;
            byte[] data = text.getBytes(java.nio.charset.StandardCharsets.UTF_8);
            for (String mode : new String[]{"wt", "w", "rwt"}) {
                try (OutputStream out = getContentResolver().openOutputStream(Uri.parse(u), mode)) { if (out == null) continue; out.write(data); out.flush(); return true; }
                catch (Exception ignored) { }
            }
            return false; }
        /** MUIS halal directory search (Azli, 20 Oct 2026): the same request halal.muis.gov.sg/halal/establishments makes
         *  (open the page for its anti-forgery token and cookies, then POST {"text": ...}). The reply goes to window.__halal(id, json). */
        @JavascriptInterface public void halalSearch(final String id, final String text) {
            new Thread(() -> {
                String out;
                try {
                    java.net.CookieManager cm = new java.net.CookieManager();
                    String ua = "Mozilla/5.0 (Linux; Android " + Build.VERSION.RELEASE + ") AppleWebKit/537.36 Chrome/126 Mobile Safari/537.36";
                    java.net.URL pu = new java.net.URL("https://halal.muis.gov.sg/halal/establishments");
                    java.net.HttpURLConnection c = (java.net.HttpURLConnection) pu.openConnection();
                    c.setRequestProperty("User-Agent", ua); c.setConnectTimeout(15000); c.setReadTimeout(20000);
                    String page = readAll(c.getInputStream());
                    java.util.List<String> sc = c.getHeaderFields().get("Set-Cookie"); if (sc != null) for (String h : sc) for (java.net.HttpCookie hc : java.net.HttpCookie.parse(h)) cm.getCookieStore().add(pu.toURI(), hc);
                    java.util.regex.Matcher m = java.util.regex.Pattern.compile("name=\"__RequestVerificationToken\" type=\"hidden\" value=\"([^\"]+)\"").matcher(page);
                    if (!m.find()) throw new Exception("token");
                    StringBuilder ck = new StringBuilder(); for (java.net.HttpCookie hc : cm.getCookieStore().getCookies()) { if (ck.length() > 0) ck.append("; "); ck.append(hc.getName()).append('=').append(hc.getValue()); }
                    java.net.HttpURLConnection p = (java.net.HttpURLConnection) new java.net.URL("https://halal.muis.gov.sg/api/halal/establishments").openConnection();
                    p.setRequestMethod("POST"); p.setDoOutput(true); p.setConnectTimeout(15000); p.setReadTimeout(25000);
                    p.setRequestProperty("User-Agent", ua); p.setRequestProperty("Content-Type", "application/json"); p.setRequestProperty("Accept", "application/json");
                    p.setRequestProperty("X-CSRF-TOKEN", m.group(1)); p.setRequestProperty("Referer", pu.toString()); p.setRequestProperty("Cookie", ck.toString());
                    JSONObject body = new JSONObject(); body.put("text", text == null ? "" : text);
                    try (OutputStream os = p.getOutputStream()) { os.write(body.toString().getBytes(java.nio.charset.StandardCharsets.UTF_8)); }
                    if (p.getResponseCode() != 200) throw new Exception("HTTP " + p.getResponseCode());
                    out = readAll(p.getInputStream());
                } catch (Exception e) { out = "{\"error\":" + JSONObject.quote(e.getClass().getSimpleName() + " " + (e.getMessage() == null ? "" : e.getMessage())) + "}"; }
                js("window.__halal && window.__halal(" + JSONObject.quote(id) + "," + JSONObject.quote(out) + ")");
            }, "halal").start(); }
        @JavascriptInterface public String deviceName() { return Build.MANUFACTURER + " " + Build.MODEL; }
        @JavascriptInterface public String takeBackup() { String s = openedBackup; openedBackup = null; return s == null ? "" : s; }
        @JavascriptInterface public void removeAdhan(String slot) { File f = AdhanService.adhanFile(MainActivity.this, slot); if (f != null) f.delete(); }
        /** Test the alert as it will really be: it follows the phone's sound mode (returns "ring", "vibrate" or "silent"). */
        @JavascriptInterface public String testSound(String sound) {
            if ("none".equals(sound)) return "none";
            if ("silent".equals(sound)) {   // Notification only: a notification with no sound and no vibration
                try { PrayerAlarms.channels(MainActivity.this);
                    android.app.NotificationManager nm = (android.app.NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
                    android.app.Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new android.app.Notification.Builder(MainActivity.this, PrayerAlarms.CH_SILENT) : new android.app.Notification.Builder(MainActivity.this);
                    b.setSmallIcon(R.drawable.ic_stat_prayer).setContentTitle("Test").setContentText("Notification only: no sound").setAutoCancel(true);
                    if (Build.VERSION.SDK_INT < 26) b.setSound(null).setVibrate(null);
                    if (nm != null) nm.notify(77, b.build()); } catch (Exception ignored) { }
                return "notify"; }
            int mode = PrayerAlarms.soundMode(MainActivity.this);
            if (mode == 1) {
                try { android.os.Vibrator v = (android.os.Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
                    if (v != null) { if (Build.VERSION.SDK_INT >= 26) v.vibrate(android.os.VibrationEffect.createWaveform(PrayerAlarms.VIBRATE, -1)); else v.vibrate(PrayerAlarms.VIBRATE, -1); } } catch (Exception ignored) { }
                return "vibrate"; }
            if (mode == 0) return "silent";
            Intent s = new Intent(MainActivity.this, AdhanService.class).putExtra("sound", sound).putExtra("title", "Test").putExtra("text", "This is how the prayer alert will sound");
            if (Build.VERSION.SDK_INT >= 26) startForegroundService(s); else startService(s);
            return "ring"; }
        @JavascriptInterface public void stopSound() { startService(new Intent(MainActivity.this, AdhanService.class).setAction("stop")); }
        @JavascriptInterface public void getLocation() {
            runOnUiThread(() -> {
                if (checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{Manifest.permission.ACCESS_COARSE_LOCATION, Manifest.permission.ACCESS_FINE_LOCATION}, REQ_LOC); return; }
                findLocation(); }); }
        @JavascriptInterface public void startCompass(double lat, double lng) {
            runOnUiThread(() -> {
                try { decl = new GeomagneticField((float) lat, (float) lng, 0f, System.currentTimeMillis()).getDeclination(); } catch (Exception e) { decl = 0f; }
                sm = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
                Sensor rv = sm == null ? null : sm.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);
                if (rv == null) { js("window.__compass && window.__compass(null,-1)"); return; }
                if (compassL != null) sm.unregisterListener(compassL);
                compassL = new SensorEventListener() {
                    final float[] R = new float[9], o = new float[3];
                    int acc = 3;
                    @Override public void onSensorChanged(SensorEvent e) {
                        long now = SystemClock.uptimeMillis(); if (now - lastCompass < 50) return; lastCompass = now;
                        SensorManager.getRotationMatrixFromVector(R, e.values); SensorManager.getOrientation(R, o);
                        float az = (float) Math.toDegrees(o[0]) + decl; az = (az + 360f) % 360f;
                        js("window.__compass && window.__compass(" + az + "," + acc + ")"); }
                    @Override public void onAccuracyChanged(Sensor s, int a) { acc = a; }
                };
                sm.registerListener(compassL, rv, SensorManager.SENSOR_DELAY_GAME);
                Sensor mag = sm.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);   // its accuracy says whether the compass needs calibrating
                if (mag != null) sm.registerListener(new SensorEventListener() {
                    @Override public void onSensorChanged(SensorEvent e) { }
                    @Override public void onAccuracyChanged(Sensor s, int a) { if (compassL != null) compassL.onAccuracyChanged(s, a); } }, mag, SensorManager.SENSOR_DELAY_UI);
            }); }
        @JavascriptInterface public void stopCompass() { runOnUiThread(() -> { if (sm != null && compassL != null) sm.unregisterListener(compassL); compassL = null; }); }
    }

    private void openAppSettings() { try { startActivity(new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + getPackageName()))); } catch (Exception ignored) { } }

    private void sendLoc(Location l) {
        if (l == null) { js("window.__loc && window.__loc(null)"); return; }
        js("window.__loc && window.__loc({lat:" + l.getLatitude() + ",lng:" + l.getLongitude() + ",acc:" + l.getAccuracy() + ",t:" + l.getTime() + "})"); }

    @SuppressWarnings("MissingPermission")
    private void findLocation() {
        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        if (lm == null) { sendLoc(null); return; }
        Location best = null;
        for (String p : lm.getProviders(true)) { try { Location l = lm.getLastKnownLocation(p); if (l != null && (best == null || l.getTime() > best.getTime())) best = l; } catch (Exception ignored) { } }
        if (best != null && System.currentTimeMillis() - best.getTime() < 30 * 60 * 1000L) { sendLoc(best); return; }
        String prov = lm.isProviderEnabled(LocationManager.NETWORK_PROVIDER) ? LocationManager.NETWORK_PROVIDER : lm.isProviderEnabled(LocationManager.GPS_PROVIDER) ? LocationManager.GPS_PROVIDER : null;
        if (prov == null) { sendLoc(best); return; }
        final Location fallback = best; final boolean[] done = {false};
        try {
            LocationListener ll = new LocationListener() {
                @Override public void onLocationChanged(Location l) { if (!done[0]) { done[0] = true; sendLoc(l); } lm.removeUpdates(this); }
                @Override public void onStatusChanged(String p, int s, Bundle b) { }
                @Override public void onProviderEnabled(String p) { }
                @Override public void onProviderDisabled(String p) { }
            };
            lm.requestLocationUpdates(prov, 0, 0, ll, getMainLooper());
            web.postDelayed(() -> { if (!done[0]) { done[0] = true; lm.removeUpdates(ll); sendLoc(fallback); } }, 20000);
        } catch (Exception e) { sendLoc(fallback); }
    }

    static boolean isOnyx() {
        String m = Build.MANUFACTURER == null ? "" : Build.MANUFACTURER.toLowerCase(), b = Build.BRAND == null ? "" : Build.BRAND.toLowerCase();
        return m.contains("onyx") || b.contains("onyx") || b.contains("boox"); }
    private com.onyx.android.sdk.pen.TouchHelper bxHelper; private boolean bxOpened = false; private float bxDensity = 1f, bxMaxP = 0f;
    private void bxSend(String ev, com.onyx.android.sdk.pen.data.TouchPointList list) {
        if (list == null || list.getPoints() == null || list.getPoints().isEmpty()) return;
        if (bxMaxP <= 0f) { try { bxMaxP = com.onyx.android.sdk.api.device.epd.EpdController.getMaxTouchPressure(); } catch (Throwable t) { bxMaxP = 4096f; } if (bxMaxP <= 0f) bxMaxP = 4096f; }
        StringBuilder sb = new StringBuilder("[");
        for (com.onyx.android.sdk.data.note.TouchPoint p : list.getPoints()) { if (sb.length() > 1) sb.append(','); sb.append('[').append(Math.round(p.x * 10) / 10f).append(',').append(Math.round(p.y * 10) / 10f).append(',').append(Math.round(Math.max(0.05f, Math.min(1f, p.pressure / bxMaxP)) * 100) / 100f).append(']'); }
        sb.append(']');
        js("window.__boox && window.__boox('" + ev + "'," + sb + "," + web.getWidth() + ")"); }
    private final com.onyx.android.sdk.pen.RawInputCallback bxCb = new com.onyx.android.sdk.pen.RawInputCallback() {
        @Override public void onBeginRawDrawing(boolean b, com.onyx.android.sdk.data.note.TouchPoint p) { }
        @Override public void onEndRawDrawing(boolean b, com.onyx.android.sdk.data.note.TouchPoint p) { }
        @Override public void onRawDrawingTouchPointMoveReceived(com.onyx.android.sdk.data.note.TouchPoint p) { }
        @Override public void onRawDrawingTouchPointListReceived(com.onyx.android.sdk.pen.data.TouchPointList l) { bxSend("stroke", l); }
        @Override public void onBeginRawErasing(boolean b, com.onyx.android.sdk.data.note.TouchPoint p) { }
        @Override public void onEndRawErasing(boolean b, com.onyx.android.sdk.data.note.TouchPoint p) { }
        @Override public void onRawErasingTouchPointMoveReceived(com.onyx.android.sdk.data.note.TouchPoint p) { }
        @Override public void onRawErasingTouchPointListReceived(com.onyx.android.sdk.pen.data.TouchPointList l) { bxSend("erase", l); }
    };
    private static final String G_SCOPE = "https://www.googleapis.com/auth/drive.appdata", G_FILE = "MyPersonalQuran-sync.json";
    private com.google.android.gms.auth.api.identity.AuthorizationRequest gReq() {
        return com.google.android.gms.auth.api.identity.AuthorizationRequest.builder()
            .setRequestedScopes(java.util.Collections.singletonList(new com.google.android.gms.common.api.Scope(G_SCOPE))).build(); }
    /** After sign-in: find the account's e-mail (Drive "about"), remember it, and tell the page. */
    private void gAfterAuth(String token) {
        new Thread(() -> { String mail = "";
            try { JSONObject o = new JSONObject(gHttp("GET", "https://www.googleapis.com/drive/v3/about?fields=user(emailAddress)", token, null, null));
                  mail = o.getJSONObject("user").optString("emailAddress", ""); } catch (Exception ignored) { }
            if (mail.isEmpty()) mail = "Google account";
            PrayerAlarms.prefs(this).edit().putString("gsync", mail).remove("gfile").apply();
            js("window.__gSigned && window.__gSigned(" + JSONObject.quote(mail) + ")"); }).start(); }
    /** A fresh access token without showing anything; null when the person must sign in again. Called off the main thread. */
    private String gToken() {
        try { com.google.android.gms.auth.api.identity.AuthorizationResult r = com.google.android.gms.tasks.Tasks.await(
                  com.google.android.gms.auth.api.identity.Identity.getAuthorizationClient(this).authorize(gReq()), 30, java.util.concurrent.TimeUnit.SECONDS);
              return r.hasResolution() ? null : r.getAccessToken(); } catch (Exception e) { return null; } }
    private static String gHttp(String method, String url, String token, String type, byte[] body) throws Exception {
        java.net.HttpURLConnection c = (java.net.HttpURLConnection) new java.net.URL(url).openConnection();
        if ("PATCH".equals(method)) { c.setRequestMethod("POST"); c.setRequestProperty("X-HTTP-Method-Override", "PATCH"); } else c.setRequestMethod(method);
        c.setRequestProperty("Authorization", "Bearer " + token); c.setConnectTimeout(15000); c.setReadTimeout(30000); c.setUseCaches(false);
        if (body != null) { c.setDoOutput(true); c.setRequestProperty("Content-Type", type); try (OutputStream o = c.getOutputStream()) { o.write(body); } }
        int code = c.getResponseCode();
        if (code >= 300) { String err = ""; try { err = readAll(c.getErrorStream()); } catch (Exception ignored) { } throw new Exception("HTTP " + code + " " + err); }
        return readAll(c.getInputStream()); }
    /** The sync file's id in the hidden app folder (newest if two devices ever created one each), or "" if none yet. */
    private String gFileId(String token) throws Exception {
        String q = java.net.URLEncoder.encode("name='" + G_FILE + "' and trashed=false", "UTF-8");
        org.json.JSONArray a = new JSONObject(gHttp("GET", "https://www.googleapis.com/drive/v3/files?spaces=appDataFolder&orderBy=modifiedTime%20desc&fields=files(id)&q=" + q, token, null, null)).getJSONArray("files");
        return a.length() > 0 ? a.getJSONObject(0).getString("id") : ""; }
    private String gRead() {
        String token = gToken(); if (token == null) return "!sign in again";
        try { String id = gFileId(token); if (id.isEmpty()) return "";
              return gHttp("GET", "https://www.googleapis.com/drive/v3/files/" + id + "?alt=media", token, null, null); }
        catch (Exception e) { return "!" + e.getMessage(); } }
    private boolean gWrite(String text) {
        String token = gToken(); if (token == null) return false;
        try { byte[] data = text.getBytes(java.nio.charset.StandardCharsets.UTF_8); String id = gFileId(token);
              if (!id.isEmpty()) { gHttp("PATCH", "https://www.googleapis.com/upload/drive/v3/files/" + id + "?uploadType=media", token, "application/json", data); return true; }
              String b = "mpqboundary", meta = "{\"name\":\"" + G_FILE + "\",\"parents\":[\"appDataFolder\"]}";
              java.io.ByteArrayOutputStream bo = new java.io.ByteArrayOutputStream();
              bo.write(("--" + b + "\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n" + meta + "\r\n--" + b + "\r\nContent-Type: application/json\r\n\r\n").getBytes(java.nio.charset.StandardCharsets.UTF_8));
              bo.write(data); bo.write(("\r\n--" + b + "--").getBytes(java.nio.charset.StandardCharsets.UTF_8));
              gHttp("POST", "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", token, "multipart/related; boundary=" + b, bo.toByteArray()); return true; }
        catch (Exception e) { return false; } }

    /* S Pen side button (Azli, 22 Oct 2026). Samsung reports a touch made while the button is held with its own actions
       (211 down, 212 up, 213 move) that the WebView ignores, so the pen drew nothing. They are turned back into ordinary
       touches, and the page is told the button is held (window.__penBtn) so the Notepad erases. Other phones report the
       button in the button state, or the pen's eraser end as its own tool. */
    private boolean penBtn = false;
    private void setPenBtn(boolean b) { if (b != penBtn) { penBtn = b; js("window.__penBtn=" + (b ? 1 : 0) + ";window.__penBtnSet&&window.__penBtnSet(" + (b ? 1 : 0) + ")"); } }
    private void penState(android.view.MotionEvent ev) {
        boolean b = (ev.getButtonState() & (android.view.MotionEvent.BUTTON_STYLUS_PRIMARY | android.view.MotionEvent.BUTTON_STYLUS_SECONDARY)) != 0;
        for (int i = 0; i < ev.getPointerCount(); i++) if (ev.getToolType(i) == android.view.MotionEvent.TOOL_TYPE_ERASER) b = true;
        if (ev.getToolType(0) == android.view.MotionEvent.TOOL_TYPE_STYLUS || ev.getToolType(0) == android.view.MotionEvent.TOOL_TYPE_ERASER) setPenBtn(b); }
    @Override public boolean dispatchTouchEvent(android.view.MotionEvent ev) {
        int a = ev.getActionMasked();
        if (a == 211 || a == 212 || a == 213) {
            android.view.MotionEvent c = android.view.MotionEvent.obtain(ev);
            c.setAction(a == 211 ? android.view.MotionEvent.ACTION_DOWN : a == 212 ? android.view.MotionEvent.ACTION_UP : android.view.MotionEvent.ACTION_MOVE);
            setPenBtn(true); boolean r = super.dispatchTouchEvent(c); c.recycle(); return r; }
        penState(ev); return super.dispatchTouchEvent(ev); }
    @Override public boolean dispatchGenericMotionEvent(android.view.MotionEvent ev) { penState(ev); return super.dispatchGenericMotionEvent(ev); }

    @Override
    protected void onActivityResult(int req, int res, Intent data) {
        super.onActivityResult(req, res, data);
        if (req == REQ_CAM) { runScan(res == RESULT_OK ? camUri : null, scanLang); return; }
        if (req == REQ_IMG) { runScan(res == RESULT_OK && data != null ? data.getData() : null, scanLang); return; }
        if (req == REQ_GAUTH) {
            if (res != RESULT_OK || data == null) { js("window.__gSigned && window.__gSigned('')"); return; }
            try { gAfterAuth(com.google.android.gms.auth.api.identity.Identity.getAuthorizationClient(this).getAuthorizationResultFromIntent(data).getAccessToken()); }
            catch (Exception e) { js("window.__gSigned && window.__gSigned('!'+" + JSONObject.quote(String.valueOf(e.getMessage())) + ")"); }
            return;
        }
        if (req == REQ_SYNC) {
            String name = "";
            if (res == RESULT_OK && data != null && data.getData() != null) {
                Uri u = data.getData();
                try { getContentResolver().takePersistableUriPermission(u, Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION); } catch (Exception ignored) { }
                try (android.database.Cursor c = getContentResolver().query(u, null, null, null, null)) { if (c != null && c.moveToFirst()) { int i = c.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME); if (i >= 0) name = c.getString(i); } } catch (Exception ignored) { }
                if (name == null || name.isEmpty()) name = "sync file";
                PrayerAlarms.prefs(this).edit().putString("syncUri", u.toString()).putString("syncName", name).apply();
            }
            js("window.__syncPicked && window.__syncPicked(" + JSONObject.quote(name) + ")"); return;
        }
        if (req == REQ_SAVE) {
            boolean ok = false; String text = pendingBackup; pendingBackup = null;
            File pf = new File(getCacheDir(), "pending-backup.json");
            if (text == null && pf.exists()) { try { text = readAll(new java.io.FileInputStream(pf)); } catch (Exception ignored) { } }
            pf.delete();
            if (res == RESULT_OK && data != null && data.getData() != null && text != null) {
                try (OutputStream out = getContentResolver().openOutputStream(data.getData(), "wt")) { out.write(text.getBytes(java.nio.charset.StandardCharsets.UTF_8)); ok = true; } catch (Exception e) { ok = false; }
            }
            js("window.__backupSaved && window.__backupSaved(" + ok + ")"); return;
        }
        if (req == REQ_OPEN) {
            boolean ok = false; openedBackup = null;
            if (res == RESULT_OK && data != null && data.getData() != null) {
                try (InputStream in = getContentResolver().openInputStream(data.getData())) {
                    java.io.ByteArrayOutputStream bo = new java.io.ByteArrayOutputStream(); byte[] b = new byte[16384]; int n; long total = 0;
                    while ((n = in.read(b)) > 0) { bo.write(b, 0, n); total += n; if (total > 20_000_000) throw new Exception("too big"); }
                    openedBackup = new String(bo.toByteArray(), java.nio.charset.StandardCharsets.UTF_8); ok = true;
                } catch (Exception e) { ok = false; }
            }
            js("window.__backupOpened && window.__backupOpened(" + ok + ")"); return;
        }
        if (req != REQ_PICK) return;
        String slot = pickSlot; pickSlot = null; String name = "";
        if (slot != null && res == RESULT_OK && data != null && data.getData() != null) {
            try {
                Uri u = data.getData();
                String disp = null;
                try (android.database.Cursor c = getContentResolver().query(u, null, null, null, null)) { if (c != null && c.moveToFirst()) { int i = c.getColumnIndex(android.provider.OpenableColumns.DISPLAY_NAME); if (i >= 0) disp = c.getString(i); } }
                String ext = disp != null && disp.contains(".") ? disp.substring(disp.lastIndexOf('.')).toLowerCase() : ".mp3";
                File dir = new File(getFilesDir(), "adhan"); dir.mkdirs();
                File old = AdhanService.adhanFile(this, slot); if (old != null) old.delete();
                File f = new File(dir, slot + ext);
                try (InputStream in = getContentResolver().openInputStream(u); OutputStream out = new FileOutputStream(f)) { byte[] b = new byte[16384]; int n; while ((n = in.read(b)) > 0) out.write(b, 0, n); }
                name = disp == null ? f.getName() : disp;
                PrayerAlarms.prefs(this).edit().putString("name_" + slot, name).apply();
            } catch (Exception e) { name = ""; }
        }
        js("window.__adhanPicked && window.__adhanPicked(" + JSONObject.quote(slot == null ? "" : slot) + "," + JSONObject.quote(name) + ")");
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

    /** Long-press text: a "Makna" (meaning) item first in the selection menu, answered inside the app (Azli, 17 Oct 2026). */
    @Override
    public void onActionModeStarted(ActionMode mode) {
        super.onActionModeStarted(mode);
        try {
            Menu m = mode.getMenu();
            if (m != null && m.findItem(0x4d4b) == null) {
                MenuItem it = m.add(Menu.NONE, 0x4d4b, 0, "Makna");
                it.setShowAsAction(MenuItem.SHOW_AS_ACTION_IF_ROOM);
                it.setOnMenuItemClickListener(x -> {
                    if (web != null) web.evaluateJavascript("(function(){var t=String(window.getSelection()||'');window.__meaning&&window.__meaning(t);})()", null);
                    mode.finish();
                    return true;
                });
            }
        } catch (Throwable ignored) { }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) web.evaluateJavascript("window.__resume && window.__resume()", null);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (recognizer != null) recognizer.cancel();
        stopPump();
        recStandaloneStop();
        btRouteOff();
        try { if (bxHelper != null && bxOpened) bxHelper.setRawDrawingEnabled(false); } catch (Throwable ignored) { }
        web.evaluateJavascript("window.__pause && window.__pause()", null);
    }

    @Override
    protected void onDestroy() {
        if (recognizer != null) { recognizer.destroy(); recognizer = null; }
        stopPump();
        btRouteOff();
        PlaybackService.hide();
        if (msess != null) { msess.release(); msess = null; }
        if (sm != null && compassL != null) sm.unregisterListener(compassL);
        web.destroy();
        super.onDestroy();
    }
}
