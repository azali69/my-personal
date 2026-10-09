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
                if ("adhan".equals(kind) && !"silent".equals(sound)) {
                    Intent s = new Intent(c, AdhanService.class).putExtra("sound", sound).putExtra("title", o.optString("title")).putExtra("text", o.optString("text"));
                    if (Build.VERSION.SDK_INT >= 26) c.startForegroundService(s); else c.startService(s);
                } else {
                    PrayerAlarms.channels(c);
                    String ch = "adhan".equals(kind) ? PrayerAlarms.CH_SILENT : PrayerAlarms.CH_REMIND;
                    PendingIntent open = PendingIntent.getActivity(c, 3, new Intent(c, MainActivity.class), PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
                    Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(c, ch) : new Notification.Builder(c);
                    b.setSmallIcon(R.drawable.ic_stat_prayer).setContentTitle(o.optString("title")).setContentText(o.optString("text"))
                     .setContentIntent(open).setAutoCancel(true).setCategory(Notification.CATEGORY_REMINDER);
                    NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
                    if (nm != null) nm.notify((int) (at / 1000 % 100000), b.build());
                }
            }
        } catch (Exception ignored) { }
        PrayerAlarms.schedule(c);
    }
}
