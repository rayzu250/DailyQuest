# Help and themed notifications

In-game notifications now use 40 px text, a 960 px panel with thematic contrast,
multiline layout and 5–14 seconds of reading time based on message length.
These are virtual coordinates in the 1080 x 1920 interface and respect the font preference.

Help opens a dismissible, scrollable topic selector. Primary has five topics with
simple instructions; secondary has six topics covering Agile, Kanban, Kaizen,
priorities, time estimates and weekly reflection. Each has a short explanation
and a practical follow-up. Kanban explicitly explains that a board is not yet
implemented. Help is also available from the navigation menu when the guide is hidden.

Android resources include ten existing character PNGs reused unchanged as large
icons and ten native vector silhouettes as small monochrome icons. Large images
are decoded with subsampling to bound memory usage. The OS controls final rendering.
Theme state is stored independently of alarm specifications: changing worlds does
not cancel or reschedule a delayed reminder. Already delivered notifications keep
their image; pending reminders use the latest synchronized theme, including after
process shutdown. Legacy schedules without a stored theme default to forest.

The existing RAPT configuration includes android/native/res. A NEW Android build
is required to install the Java changes and images. No APK was built for this update.

Validation: Ren'Py 8.5.3 lint passed; isolated help_notifications UI testcase passed
(four assertions), with primary/secondary help and enlarged-notification screenshots
reviewed. Java compiled against Android 36 with JDK 21. AAPT2 compiled all native
resources. Notification delivery and OEM icon display still require device testing.
No commits or pushes were created.
