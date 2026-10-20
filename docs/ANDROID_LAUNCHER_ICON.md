# Android launcher icon

The approved journal-and-star artwork is now wired into Ren'Py RAPT through
android-icon_background.png and android-icon_foreground.png at the project root.
Previously it existed only under art/android and was not consumed by RAPT.

Run tools/prepare_android_icon.ps1 to reproduce the assets with Windows System.Drawing.
The original artwork is preserved. Both layers are 1080 x 1080; the artwork is inset
on an opaque green background and the foreground is transparent. This is a static
adaptive icon, not independently animated/parallax artwork. RAPT generates the five
launcher densities and the legacy masked icon, using its existing adaptive-icon XML.
Keep update_icons and update_always enabled in the local Android configuration.

Rebuild and install the APK over the existing application to see the new icon.
Do not uninstall merely to refresh the launcher icon, since uninstalling removes
local task data. Launcher refresh behavior depends on the phone.

Validation: the SDK generated the journal-and-star launcher icon at xxxhdpi and it
was visually inspected. APK build status is recorded separately in the task response.
No commit or push has been made for this change.
