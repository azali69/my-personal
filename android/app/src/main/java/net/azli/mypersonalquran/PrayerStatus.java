package net.azli.mypersonalquran;

import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Today's prayer times in the notification bar (Azli, 13 Oct 2026): always, or from 30 minutes before each prayer.
 * The app hands over three weeks of days (times as moments, and as text in the place's own clock); this keeps the
 * notification up to date at each prayer time, 30 minutes before it, and at midnight.
 */
public class PrayerStatus extends BroadcastReceiver {
    static final String CH = "prayer_bar";
    static final int ID = 79;

    @Override public void onReceive(Context c, Intent i) { update(c); }

    static void save(Context c, String json, String mode) {
        PrayerAlarms.prefs(c).edit().putString("status_days", json).putString("status_mode", mode == null ? "always" : mode).apply();
        update(c);
    }

    static void update(Context c) {
        NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
        if (nm == null) return;
        String mode = PrayerAlarms.prefs(c).getString("status_mode", "always");
        long now = System.currentTimeMillis();
        JSONObject today = null, tomorrow = null;
        long wake = 0;
        try {
            JSONArray days = new JSONArray(PrayerAlarms.prefs(c).getString("status_days", "[]"));
            for (int k = 0; k < days.length(); k++) {
                JSONObject d = days.getJSONObject(k);
                long day = d.optLong("day");
                if (day <= now && now < day + 86400000L) { today = d; if (k + 1 < days.length()) tomorrow = days.getJSONObject(k + 1); }
                JSONArray t = d.optJSONArray("times");
                if (t != null) for (int j = 0; j < t.length(); j++) {
                    long at = t.optLong(j);
                    if (at <= 0) continue;
                    for (long w : new long[]{at, at - 30 * 60000L}) if (w > now + 1000 && (wake == 0 || w < wake)) wake = w;
                }
                if (day + 86400000L > now + 1000 && (wake == 0 || day + 86400000L < wake)) wake = day + 86400000L;
            }
        } catch (Exception e) { today = null; }
        schedule(c, wake);
        if ("off".equals(mode) || today == null) { nm.cancel(ID); return; }
        // the next prayer (Syuruk is shown but is not a prayer)
        String nextName = null, nextShown = null; long nextAt = 0;
        JSONArray names = today.optJSONArray("names"), times = today.optJSONArray("times"), shown = today.optJSONArray("shown");
        for (int j = 0; times != null && j < times.length(); j++) {
            if (j == 1) continue;
            long at = times.optLong(j);
            if (at > now) { nextAt = at; nextName = names.optString(j); nextShown = shown.optString(j); break; }
        }
        if (nextAt == 0 && tomorrow != null) {
            JSONArray t2 = tomorrow.optJSONArray("times"), s2 = tomorrow.optJSONArray("shown"), n2 = tomorrow.optJSONArray("names");
            if (t2 != null && t2.optLong(0) > 0) { nextAt = t2.optLong(0); nextName = n2.optString(0); nextShown = s2.optString(0) + " (tomorrow)"; }
        }
        if ("before".equals(mode) && (nextAt == 0 || nextAt - now > 30 * 60000L)) { nm.cancel(ID); return; }
        if (Build.VERSION.SDK_INT >= 26) {
            NotificationChannel ch = new NotificationChannel(CH, "Prayer times in the notification bar", NotificationManager.IMPORTANCE_LOW);
            ch.setDescription("Today's prayer times and the time left to the next prayer");
            ch.setSound(null, null); ch.enableVibration(false); ch.setShowBadge(false);
            nm.createNotificationChannel(ch);
        }
        StringBuilder line = new StringBuilder();
        for (int j = 0; names != null && j < names.length(); j++) {
            if (line.length() > 0) line.append("  ·  ");
            line.append(names.optString(j)).append(' ').append(shown.optString(j).replace(" am", "").replace(" pm", ""));
        }
        PendingIntent open = PendingIntent.getActivity(c, 8, new Intent(c, MainActivity.class).putExtra("open", "prayer").addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP),
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification.Builder b = Build.VERSION.SDK_INT >= 26 ? new Notification.Builder(c, CH) : new Notification.Builder(c);
        b.setSmallIcon(R.drawable.ic_stat_prayer).setOngoing(true).setOnlyAlertOnce(true).setShowWhen(nextAt > 0)
         .setContentTitle(nextName == null ? "Prayer times" : "Next: " + nextName + "  " + nextShown)
         .setContentText(line.toString()).setSubText(today.optString("title"))
         .setStyle(new Notification.BigTextStyle().bigText(line.toString()))
         .setContentIntent(open).setVisibility(Notification.VISIBILITY_PUBLIC).setCategory(Notification.CATEGORY_STATUS);
        if (Build.VERSION.SDK_INT < 26) b.setPriority(Notification.PRIORITY_LOW);
        if (nextAt > 0) { b.setWhen(nextAt).setUsesChronometer(true); if (Build.VERSION.SDK_INT >= 24) b.setChronometerCountDown(true); }
        try { nm.notify(ID, b.build()); } catch (Exception ignored) { }
    }

    private static void schedule(Context c, long at) {
        AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        PendingIntent pi = PendingIntent.getBroadcast(c, 9, new Intent(c, PrayerStatus.class).setAction("net.azli.mypersonalquran.STATUS"),
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        am.cancel(pi);
        if (at <= 0) return;
        try {
            if (PrayerAlarms.canExact(c) && Build.VERSION.SDK_INT >= 23) am.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, pi);
            else if (Build.VERSION.SDK_INT >= 23) am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, at, pi);
            else am.set(AlarmManager.RTC_WAKEUP, at, pi);
        } catch (Exception ignored) { }
    }
}
