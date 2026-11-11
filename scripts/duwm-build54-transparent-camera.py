from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
old='indicator=txt("CAMERA INITIALISING",10);indicator.setSingleLine(true);'
# Previous camera patch already adds accessibility after setSingleLine; insert only transparent camera status treatment.
if s.count(old)!=1:raise RuntimeError('Camera status setup not found')
s=s.replace(old,old+'indicator.setBackgroundColor(android.graphics.Color.TRANSPARENT);')
# Make recording profile read cleanly over live preview without a solid blue background.
old2='recordingProfile=txt(profileLabel(),10);recordingProfile.setGravity(Gravity.CENTER);'
if s.count(old2)!=1:raise RuntimeError('Recording profile setup not found')
s=s.replace(old2,old2+'recordingProfile.setBackgroundColor(android.graphics.Color.TRANSPARENT);')
# Validate recorded file after recording; do not claim that byte size proves playable MP4 or burnt-in telemetry.
old3='indicator.setText(valid?"● VIDEO CAPTURED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");'
if s.count(old3)!=1:raise RuntimeError('Recording outcome target missing')
s=s.replace(old3,'indicator.setText(valid?"● VIDEO CAPTURED / REVIEW IN GALLERY":"● VIDEO ERROR / RETRY");')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.52"'
if v.count(old)!=1:raise RuntimeError('Build 52 version missing')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.54"'))
print('Build 54: transparent camera status and profile backgrounds; review-in-gallery message; original recording engine unchanged')
