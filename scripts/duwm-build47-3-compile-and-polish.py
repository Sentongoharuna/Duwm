from pathlib import Path
import sys
root=Path(sys.argv[1]);java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=java/'RunningballV20LiveFeedPulse.java';s=p.read_text()
bad='c.meta.setText("SOURCE  "+PROVIDER[i]+"\n"+v.note);'
if s.count(bad)!=1:raise RuntimeError('Expected 47.2 malformed Java string not found')
s=s.replace(bad,'c.meta.setText("SOURCE  "+PROVIDER[i]+"\\n"+v.note);')
# Make source health status legible and avoid excessive animations.
old='c.dot.animate().cancel();c.dot.clearAnimation();'
new='c.dot.animate().cancel();c.dot.clearAnimation();c.dot.setContentDescription(category+" signal");'
if s.count(old)!=1:raise RuntimeError('Signal anchor mismatch')
s=s.replace(old,new)
old='c.meta.setMaxLines(2);c.meta.setEllipsize(android.text.TextUtils.TruncateAt.END);'
new='c.meta.setMaxLines(3);c.meta.setEllipsize(android.text.TextUtils.TruncateAt.END);'
if s.count(old)!=1:raise RuntimeError('Meta anchor mismatch')
s=s.replace(old,new)
p.write_text(s)
g=root/'app/build.gradle.kts';t=g.read_text()
old='versionName = "1728.2.21.4.47.2"'
if t.count(old)!=1:raise RuntimeError('Expected 47.2 version')
g.write_text(t.replace(old,'versionName = "1728.2.21.4.47.3"'))
print('Build 47.3 repaired invalid Java newline, improved three-line source attribution and status accessibility')
