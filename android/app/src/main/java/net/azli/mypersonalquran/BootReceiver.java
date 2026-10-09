package net.azli.mypersonalquran;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/** After a restart, an app update or a clock / time-zone change, set the next prayer alert again. */
public class BootReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context c, Intent intent) { PrayerAlarms.schedule(c); }
}
