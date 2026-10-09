package net.azli.mypersonalquran;

import android.app.AlarmManager;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.media.AudioAttributes;
import android.net.Uri;
import android.os.Build;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Prayer alerts. The web app sends the coming weeks' alerts as a list (time, prayer, adhan or reminder, sound);
 * only the next one is set with Android at any time. When it fires, the receiver shows it and sets the following one.
 * The list survives restarts (BootReceiver sets the next one again).
 */
public final class PrayerAlarms {
    static final String PREFS = "prayer";
    static final String CH_ADHAN = "adhan2", CH_REMIND = "reminder", CH_SILENT = "silent";

    static SharedPreferences prefs(Context c) { return c.getSharedPreferences(PREFS, Context.MODE_PRIVATE); }

    static void save(Context c, String json) { prefs(c).edit().putString("list", json).apply(); schedule(c); }

    static void channels(Context c) {
        if (Build.VERSION.SDK_INT < 26) return;
        NotificationManager nm = c.getSystemService(NotificationManager.class);
        NotificationChannel a = new NotificationChannel(CH_ADHAN, "Adhan", NotificationManager.IMPORTANCE_HIGH);
        a.setDescription("Prayer time: the adhan or the tone plays from the app");
        a.setSound(null, null);   // the sound is played by AdhanService, so the user can stop it
        NotificationChannel r = new NotificationChannel(CH_REMIND, "Reminder before prayer", NotificationManager.IMPORTANCE_HIGH);
        r.setDescription("A short alert some minutes before each prayer");
        NotificationChannel s = new NotificationChannel(CH_SILENT, "Silent prayer alert", NotificationManager.IMPORTANCE_DEFAULT);
        s.setSound(null, null);
        nm.createNotificationChannel(a); nm.createNotificationChannel(r); nm.createNotificationChannel(s);
    }

    /** The next alert after now, or null. */
    static JSONObject next(Context c, long after) {
        try {
            JSONArray l = new JSONArray(prefs(c).getString("list", "[]"));
            JSONObject best = null;
            for (int i = 0; i < l.length(); i++) {
                JSONObject o = l.getJSONObject(i);
                long at = o.optLong("at");
                if (at > after && (best == null || at < best.optLong("at"))) best = o;
            }
            return best;
        } catch (Exception e) { return null; }
    }

    static boolean canExact(Context c) {
        if (Build.VERSION.SDK_INT < 31) return true;
        AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE);
        return am != null && am.canScheduleExactAlarms();
    }

    static void schedule(Context c) {
        channels(c);
        AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        Intent i = new Intent(c, AlarmReceiver.class).setAction("net.azli.mypersonalquran.PRAYER");
        PendingIntent pi = PendingIntent.getBroadcast(c, 1, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        am.cancel(pi);
        JSONObject n = next(c, System.currentTimeMillis() + 1000);
        prefs(c).edit().putString("pending", n == null ? "" : n.toString()).apply();
        if (n == null) return;
        long at = n.optLong("at");
        if (canExact(c)) {
            // shown as an alarm clock to Android, so it is on time even in Doze, and the adhan may start from the background
            Intent open = new Intent(c, MainActivity.class);
            PendingIntent show = PendingIntent.getActivity(c, 2, open, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
            am.setAlarmClock(new AlarmManager.AlarmClockInfo(at, show), pi);
        } else {
            am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, pi);
        }
    }
}
