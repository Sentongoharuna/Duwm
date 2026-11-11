from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Build 53 camera target mismatch: '+a[:100])
 s=s.replace(a,b)
once('indicator.setText(valid?"● VIDEO CAPTURED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");',
'''indicator.setText(valid?"● VIDEO CAPTURED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");''')
# Explicitly validate a local recording file before claiming the capture is saved.
once('boolean valid=outputFile!=null&&outputFile.exists()&&outputFile.length()>1024;',
'''boolean valid=outputFile!=null&&outputFile.isFile()&&outputFile.canRead()&&outputFile.length()>4096;''')
once('if(!valid)note("Recording could not be finalized. Check storage space and retry.");',
'''if(!valid)note("MP4 verification failed: missing, unreadable or incomplete recording. Check storage and retry.");''')
# Use media metadata only as a check; don't assert the video has burnt-in telemetry.
once('indicator.setContentDescription(valid?"Recording captured; open private draft to review video":"Recording failed; retry or check available storage");',
'''indicator.setContentDescription(valid?"Recording captured; open private draft to review video":"Recording failed; retry or check available storage");''')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.52"'
if v.count(old)!=1:raise RuntimeError('Expected Build 52 version')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.53"'))
print('Build 53: strengthen local MP4 existence/readability/size validation; do not falsely certify telemetry export')
