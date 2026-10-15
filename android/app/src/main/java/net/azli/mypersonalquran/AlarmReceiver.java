package net.azli.mypersonalquran;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

import org.json.JSONObject;

/** A prayer alert is due: the adhan or tone plays (AdhanService), or a reminder notification is shown; then the next alert is set. */
public class AlarmReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context c, Intent intent) {
        try {
            JSONObject o = new JSONObject(PrayerAlarms.prefs(c).getString("pending", "{}"));
            long at = o.optLong("at");
            // ignore an alert that is more than 10 minutes late (phone was off): never sound the adhan at the wrong time
            if (at > 0 && System.currentTimeMillis() - at < 10 * 60 * 1000L) {
                String kind = o.optString("kind"), sound = o.optString("sound", "tone");
                // follow the phone's sound mode (Azli, 11 Oct 2026): ring = adhan or tone; vibrate = vibrate only; silent or
                // Do Not Disturb = a silent notification. The notification itself is always shown.
                int mode = PrayerAlarms.soundMode(c);
                if ("adhan".equals(kind) && !"silent".equals(sound) && mode == 2) {
                    Intent s = new Intent(c, AdhanService.class).putExtra("sound", sound).putExtra("title", o.optString("title")).putExtra("text", o.optString("text"));
                    if (Build.VERSION.SDK_INT >= 26) c.startForegroundService(s); else c.startService(s);
                } else {
                    PrayerAlarms.channels(c);
                    // "Notification only" means no sound at all, for the reminder too (Azli, 15 Oct 2026)
                    boolean quiet = "silent".equals(sound);
                    String ch = "adhan".equals(kind) ? (mode == 1 && !quiet ? PrayerAlarms.CH_VIBRATE : PrayerAlarms.CH_SILENT)
                            : (quiet || mode == 0 ? PrayerAlarms.CH_SILENT : mode == 1 ? PrayerAlarms.CH_VIBRATE : PrayerAlarms.CH_REMIND);
                    PendingIntent open = PendingIntent.getActivity(c, 3, new Intent(c, MainActivity.class).putExtra("open", "prayer"), PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
                    Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(c, ch) : new Notification.Builder(c);
                    b.setSmallIcon(R.drawable.ic_stat_prayer).setContentTitle(o.optString("title")).setContentText(o.optString("text"))
                     .setContentIntent(open).setAutoCancel(true).setCategory(Notification.CATEGORY_REMINDER);
                    NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
                    if (Build.VERSION.SDK_INT < 26 && PrayerAlarms.CH_VIBRATE.equals(ch)) b.setVibrate(PrayerAlarms.VIBRATE);
                    if (nm != null) nm.notify((int) (at / 1000 % 100000), b.build());
                }
            }
        } catch (Exception ignored) { }
        PrayerAlarms.schedule(c);
        PrayerStatus.update(c);
    }
}
