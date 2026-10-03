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

import java.util.ArrayList;

/**
 * Hosts the My Personal Quran web app from the APK's own assets (works offline)
 * and gives it Android's speech recogniser, because WebView has no Web Speech API.
 */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final int REQ_MIC = 7;

    private WebView web;
    private SpeechRecognizer recognizer;
    private String pendingLang;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        web.setBackgroundColor(Color.parseColor("#f4efe2"));
        setContentView(web);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setMediaPlaybackRequiresUserGesture(true);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);

        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
                .setDomain(HOST)
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        web.setWebViewClient(new WebViewClient() {
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                return loader.shouldInterceptRequest(request.getUrl());
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
            runOnUiThread(() -> { if (recognizer != null) recognizer.stopListening(); });
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
                    int f = on ? (View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION)
                               : View.SYSTEM_UI_FLAG_VISIBLE;
                    getWindow().getDecorView().setSystemUiVisibility(f);
                }
            });
        }

        @JavascriptInterface
        public void setBarColor(final String hex, final boolean dark) {
            runOnUiThread(() -> {
                try {
                    int c = Color.parseColor(hex);
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
        Intent i = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE, lang);
        i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, lang);
        i.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true);
        i.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1);
        i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 4000L);
        i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 3000L);
        i.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 15000L);
        try {
            recognizer.startListening(i);
        } catch (Exception e) {
            emitError("aborted");
            emit("onend", null);
        }
    }

    private class Listener implements RecognitionListener {
        private boolean ended;

        private void end() { if (!ended) { ended = true; emit("onend", null); } }

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
            result(first(b), true);
            end();
        }

        @Override public void onError(int error) {
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
        web.evaluateJavascript("window.__pause && window.__pause()", null);
    }

    @Override
    protected void onDestroy() {
        if (recognizer != null) { recognizer.destroy(); recognizer = null; }
        web.destroy();
        super.onDestroy();
    }
}
