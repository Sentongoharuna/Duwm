from pathlib import Path
import sys
root=Path(sys.argv[1])
cam=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=cam.read_text()
old='indicator.setText(valid?"● VIDEO CAPTURED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");'
new='''indicator.setText(valid?"● VIDEO CAPTURED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");
        indicator.setContentDescription(valid?"Recording captured; open private draft to review video":"Recording failed; retry or check available storage");'''
if s.count(old)!=1:raise RuntimeError('Build 52 camera anchor mismatch')
cam.write_text(s.replace(old,new))
gradle=root/'app/build.gradle.kts';v=gradle.read_text()
old='versionName = "1728.2.21.4.51"'
if v.count(old)!=1:raise RuntimeError('Build 51 version not found')
gradle.write_text(v.replace(old,'versionName = "1728.2.21.4.52"'))
print('Build 52: recording success/failure accessibility and verification build')
