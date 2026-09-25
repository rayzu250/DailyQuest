"""Install the package-scoped native extension in Ren'Py 8.5.3 RAPT templates.

Run again after moving the project or updating the SDK. --remove restores the
original templates only if no one has edited them since installation.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEGIN = "{# DAILYQUEST_REMINDERS_BEGIN #}"
END = "{# DAILYQUEST_REMINDERS_END #}"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def configure(sdk, remove=False):
    package = json.loads((ROOT / "android.json").read_text(encoding="utf-8-sig"))["package"]
    if not package or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._" for c in package):
        raise ValueError("Invalid Android package")
    native = (ROOT / "android/native").as_posix().replace("'", "\\'")
    manifest = '''
    <receiver android:name="com.dailyquest.reminders.ReminderReceiver" android:exported="false">
      <intent-filter>
        <action android:name="android.intent.action.BOOT_COMPLETED" />
        <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
        <action android:name="android.intent.action.TIME_SET" />
        <action android:name="android.intent.action.TIMEZONE_CHANGED" />
        <action android:name="android.app.action.SCHEDULE_EXACT_ALARM_PERMISSION_STATE_CHANGED" />
      </intent-filter>
    </receiver>
    <activity android:name="com.dailyquest.reminders.ReminderOpenActivity"
        android:exported="false" android:excludeFromRecents="true"
        android:theme="@android:style/Theme.NoDisplay" />
'''
    gradle = "\n    sourceSets { main { java.srcDir '%s/src'; res.srcDir '%s/res' } }\n" % (native, native)
    plans = []
    for name, anchor, fragment in [
            ("app-AndroidManifest.xml", "  </application>", manifest),
            ("app-build.gradle", '    compileSdkVersion = "android-36"', gradle)]:
        path = sdk / "rapt/templates" / name
        backup = path.with_name(name + ".dailyquest-original")
        checksum = path.with_name(name + ".dailyquest-sha256")
        current = path.read_bytes()
        if backup.exists():
            if not checksum.exists() or digest(current) != checksum.read_text().strip():
                raise RuntimeError("Template changed externally; review before replacing: " + str(path))
            original = backup.read_bytes()
        else:
            original = current
        source = original.decode("utf-8")
        if BEGIN in source or source.count(anchor) != 1:
            raise RuntimeError("Unrecognized SDK template: " + str(path))
        block = BEGIN + "\n{% if config.package == '" + package + "' %}\n" + fragment + "{% endif %}\n" + END + "\n"
        updated = original if remove else source.replace(anchor, block + anchor).encode("utf-8")
        plans.append((path, backup, checksum, original, updated))
    for path, backup, checksum, original, updated in plans:
        if not remove and not backup.exists():
            backup.write_bytes(original)
        path.write_bytes(updated)
        if remove:
            backup.unlink(missing_ok=True)
            checksum.unlink(missing_ok=True)
        else:
            checksum.write_text(digest(updated))
        print(("Restored: " if remove else "Configured: ") + str(path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, default=ROOT.parents[1])
    parser.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    configure(args.sdk.resolve(), args.remove)
