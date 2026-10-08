package com.dailyquest.reminders;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

/** Visible activity trampoline: Android 12 disallows notification receiver trampolines. */
public final class ReminderOpenActivity extends Activity {
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        String id = getIntent().getStringExtra("id");
        if (id != null) Reminders.openTask(this, id);
        Intent launch = getPackageManager().getLaunchIntentForPackage(getPackageName());
        if (launch != null) {
            launch.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
            startActivity(launch);
        }
        finish();
    }
}
