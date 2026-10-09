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
        PendingIntent open = PendingIntent.getActivity(this, 5, new Intent(this, MainActivity.class), PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, PrayerAlarms.CH_ADHAN) : new Notification.Builder(this);
        b.setSmallIcon(R.drawable.ic_stat_prayer).setContentTitle(title == null ? "" : title).setContentText(text == null ? "" : text)
         .setContentIntent(open).setDeleteIntent(stop).setCategory(Notification.CATEGORY_ALARM)
         .addAction(new Notification.Action.Builder(null, "Stop", stop).build());
        Notification n = b.build();
        if (Build.VERSION.SDK_INT >= 29) startForeground(77, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK); else startForeground(77, n);
        try {
            if (mp != null) { mp.release(); mp = null; }
            mp = new MediaPlayer();
            mp.setAudioAttributes(new AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_ALARM).setContentType(AudioAttributes.CONTENT_TYPE_MUSIC).build());
            File f = ("makkah".equals(sound) || "madinah".equals(sound)) ? adhanFile(this, sound) : null;
            if (f != null) mp.setDataSource(f.getPath());
            else mp.setDataSource(this, Uri.parse("android.resource://" + getPackageName() + "/" + R.raw.tone));
            mp.setOnCompletionListener(m -> stopAll());
            mp.setOnErrorListener((m, w, e) -> { stopAll(); return true; });
            mp.prepare();
            mp.start();
        } catch (Exception e) { stopAll(); }
        return START_NOT_STICKY;
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
