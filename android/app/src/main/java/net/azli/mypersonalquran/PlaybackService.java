package net.azli.mypersonalquran;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.media.session.MediaSession;
import android.net.wifi.WifiManager;
import android.os.Build;
import android.os.IBinder;
import android.os.PowerManager;

/**
 * Keeps the reciter going while the screen is off or another app is open.
 * The recitation itself plays in the app's page; without a foreground service Android may freeze the app or cut its
 * network once a surah ends, so the next surah never starts. This service shows the "now playing" notification
 * (with the lock-screen controls) and holds the CPU and Wi-Fi awake only while the reciter is playing.
 */
public class PlaybackService extends Service {
    static final String CH = "playback";
    static volatile PlaybackService instance;
    static volatile MediaSession.Token token;
    static volatile Runnable onPauseCmd, onPlayCmd, onNextCmd, onStopCmd;
    static volatile String pTitle = "", pSub = "";
    static volatile boolean pPlaying = true;

    private PowerManager.WakeLock wake;
    private WifiManager.WifiLock wifi;

    /** Start (from the app while it is open) or update the running service. */
    static void show(Context c, String title, String sub, boolean playing) {
        pTitle = title == null ? "" : title; pSub = sub == null ? "" : sub; pPlaying = playing;
        PlaybackService s = instance;
        if (s != null) { s.refresh(); return; }
        try {
            Intent i = new Intent(c, PlaybackService.class);
            if (Build.VERSION.SDK_INT >= 26) c.startForegroundService(i); else c.startService(i);
        } catch (Exception ignored) { }   // e.g. not allowed from the background: playback still works while the app is open
    }

    static void hide() { PlaybackService s = instance; if (s != null) s.end(); }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String a = intent == null ? null : intent.getAction();
        if ("pause".equals(a)) { run(onPauseCmd); return START_NOT_STICKY; }
        if ("play".equals(a)) { run(onPlayCmd); return START_NOT_STICKY; }
        if ("next".equals(a)) { run(onNextCmd); return START_NOT_STICKY; }
        if ("stop".equals(a)) { run(onStopCmd); end(); return START_NOT_STICKY; }
        instance = this;
        Notification n = build();
        try {
            if (Build.VERSION.SDK_INT >= 29) startForeground(78, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PLAYBACK); else startForeground(78, n);
        } catch (Exception e) { instance = null; stopSelf(); return START_NOT_STICKY; }
        locks(pPlaying);
        return START_NOT_STICKY;
    }

    private static void run(Runnable r) { if (r != null) try { r.run(); } catch (Exception ignored) { } }

    private void refresh() {
        try {
            NotificationManager nm = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
            if (nm != null) nm.notify(78, build());
        } catch (Exception ignored) { }
        locks(pPlaying);
    }

    private PendingIntent act(String a, int code) {
        return PendingIntent.getService(this, code, new Intent(this, PlaybackService.class).setAction(a), PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    private Notification build() {
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationManager nm = getSystemService(NotificationManager.class);
            NotificationChannel ch = new NotificationChannel(CH, "Recitation playing", NotificationManager.IMPORTANCE_LOW);
            ch.setDescription("Shown while the reciter plays, so it carries on with the screen off");
            ch.setSound(null, null);
            nm.createNotificationChannel(ch);
        }
        PendingIntent open = PendingIntent.getActivity(this, 6, new Intent(this, MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP), PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(this, CH) : new Notification.Builder(this);
        b.setSmallIcon(R.drawable.ic_stat_prayer).setContentTitle(pTitle).setContentText(pSub).setContentIntent(open)
         .setOngoing(pPlaying).setShowWhen(false).setVisibility(Notification.VISIBILITY_PUBLIC)
         .addAction(new Notification.Action.Builder(null, pPlaying ? "Pause" : "Play", act(pPlaying ? "pause" : "play", 11)).build())
         .addAction(new Notification.Action.Builder(null, "Next", act("next", 12)).build())
         .addAction(new Notification.Action.Builder(null, "Stop", act("stop", 13)).build());
        Notification.MediaStyle st = new Notification.MediaStyle().setShowActionsInCompactView(0, 1, 2);
        if (token != null) st.setMediaSession(token);
        b.setStyle(st);
        return b.build();
    }

    private void locks(boolean on) {
        try {
            if (on) {
                if (wake == null) {
                    PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
                    wake = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "MyPersonalQuran:recitation");
                    wake.setReferenceCounted(false);
                }
                if (!wake.isHeld()) wake.acquire(3 * 60 * 60 * 1000L);   // at most 3 hours at a time
                if (wifi == null) {
                    WifiManager wm = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
                    if (wm != null) { wifi = wm.createWifiLock(WifiManager.WIFI_MODE_FULL_HIGH_PERF, "MyPersonalQuran:recitation"); wifi.setReferenceCounted(false); }
                }
                if (wifi != null && !wifi.isHeld()) wifi.acquire();
            } else {
                if (wake != null && wake.isHeld()) wake.release();
                if (wifi != null && wifi.isHeld()) wifi.release();
            }
        } catch (Exception ignored) { }
    }

    private void end() {
        locks(false);
        instance = null;
        try { if (Build.VERSION.SDK_INT >= 24) stopForeground(STOP_FOREGROUND_REMOVE); else stopForeground(true); } catch (Exception ignored) { }
        stopSelf();
    }

    @Override public void onDestroy() { locks(false); if (instance == this) instance = null; super.onDestroy(); }
    @Override public IBinder onBind(Intent i) { return null; }
}
