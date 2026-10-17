package net.azli.mypersonalquran;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Build;
import android.os.IBinder;

import java.io.File;

/** Plays the adhan (the user's own Makkah / Madinah file) or the built-in tone, with a notification that can stop it. */
public class AdhanService extends Service {
    private MediaPlayer mp;

    static File adhanFile(Context c, String slot) {
        File d = new File(c.getFilesDir(), "adhan");
        File[] fs = d.listFiles();
        if (fs != null) for (File f : fs) if (f.getName().startsWith(slot + ".")) return f;
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent != null && "stop".equals(intent.getAction())) { stopAll(); return START_NOT_STICKY; }
        String sound = intent == null ? "tone" : intent.getStringExtra("sound");
        String title = intent == null ? "" : intent.getStringExtra("title");
        String text = intent == null ? "" : intent.getStringExtra("text");
        PrayerAlarms.channels(this);
        PendingIntent stop = PendingIntent.getService(this, 4, new Intent(this, AdhanService.class).setAction("stop"), PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        PendingIntent open = PendingIntent.getActivity(this, 5, new Intent(this, MainActivity.class).putExtra("open", "prayer"), PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, PrayerAlarms.CH_ADHAN) : new Notification.Builder(this);
        b.setSmallIcon(R.drawable.ic_stat_prayer).setContentTitle(title == null ? "" : title).setContentText(text == null ? "" : text)
         .setContentIntent(open).setDeleteIntent(stop).setCategory(Notification.CATEGORY_ALARM)
         .addAction(new Notification.Action.Builder(null, "Stop", stop).build());
        Notification n = b.build();
        if (Build.VERSION.SDK_INT >= 29) startForeground(77, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK); else startForeground(77, n);
        try {
            if (mp != null) { mp.release(); mp = null; }
            mp = new MediaPlayer();
            // earphones or Bluetooth connected: play there only (as media); otherwise as an alarm on the phone's speaker
            mp.setAudioAttributes(new AudioAttributes.Builder().setUsage(headset() ? AudioAttributes.USAGE_MEDIA : AudioAttributes.USAGE_ALARM).setContentType(AudioAttributes.CONTENT_TYPE_MUSIC).build());
            // "mytone:10" = the person's own sound, cut after 10 seconds (about "Allahu akbar, Allahu akbar"); tone2, tone3 = built-in
            int cut = 0; String base = sound == null ? "tone" : sound;
            if (base.startsWith("mytone")) { try { cut = Integer.parseInt(base.substring(base.indexOf(':') + 1)); } catch (Exception ignored) { cut = 10; } base = "mytone"; }
            File f = ("makkah".equals(base) || "madinah".equals(base) || "mytone".equals(base)) ? adhanFile(this, base) : null;
            int raw = "tone2".equals(base) ? R.raw.tone2 : "tone3".equals(base) ? R.raw.tone3 : R.raw.tone;
            if (f != null) mp.setDataSource(f.getPath());
            else mp.setDataSource(this, Uri.parse("android.resource://" + getPackageName() + "/" + raw));
            if (f != null && cut > 0) { final MediaPlayer me = mp; new android.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> { if (mp == me) stopAll(); }, cut * 1000L); }
            mp.setOnCompletionListener(m -> stopAll());
            mp.setOnErrorListener((m, w, e) -> { stopAll(); return true; });
            mp.prepare();
            mp.start();
        } catch (Exception e) { stopAll(); }
        return START_NOT_STICKY;
    }

    private boolean headset() {
        try {
            android.media.AudioManager am = (android.media.AudioManager) getSystemService(Context.AUDIO_SERVICE);
            if (am == null || Build.VERSION.SDK_INT < 23) return false;
            for (android.media.AudioDeviceInfo d : am.getDevices(android.media.AudioManager.GET_DEVICES_OUTPUTS)) {
                int t = d.getType();
                if (t == android.media.AudioDeviceInfo.TYPE_BLUETOOTH_A2DP || t == android.media.AudioDeviceInfo.TYPE_BLUETOOTH_SCO
                    || t == android.media.AudioDeviceInfo.TYPE_WIRED_HEADSET || t == android.media.AudioDeviceInfo.TYPE_WIRED_HEADPHONES
                    || (Build.VERSION.SDK_INT >= 26 && t == android.media.AudioDeviceInfo.TYPE_USB_HEADSET)
                    || (Build.VERSION.SDK_INT >= 31 && (t == android.media.AudioDeviceInfo.TYPE_BLE_HEADSET || t == android.media.AudioDeviceInfo.TYPE_BLE_SPEAKER))) return true;
            }
        } catch (Exception ignored) { }
        return false;
    }

    private void stopAll() {
        try { if (mp != null) { mp.stop(); mp.release(); } } catch (Exception ignored) { }
        mp = null;
        if (Build.VERSION.SDK_INT >= 24) stopForeground(STOP_FOREGROUND_DETACH); else stopForeground(false);
        stopSelf();
    }

    @Override public void onDestroy() { try { if (mp != null) mp.release(); } catch (Exception ignored) { } mp = null; super.onDestroy(); }
    @Override public IBinder onBind(Intent i) { return null; }
}
