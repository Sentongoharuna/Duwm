from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/RunningballV20LiveFeedPulse.java'
s=p.read_text()
def once(old,new):
 global s
 n=s.count(old)
 if n!=1:raise RuntimeError(f'Build 47.2 expected one anchor, found {n}: {old[:90]}')
 s=s.replace(old,new)
# Make the dashboard data age explicit and visible, while preserving actual source counts.
once('c.age.setText(category+"  ·  "+age(validTime?v.stamp:0)+(error?"  ·  ERROR":""));',
'''c.age.setText(category+"  ·  UPDATED "+age(validTime?v.stamp:0)+(error?"  ·  ERROR":""));
      c.age.setContentDescription(NAME[i]+": "+category+", last update "+age(validTime?v.stamp:0));''')
# Separate category label and provider attribution, improve information hierarchy.
once('c.meta.setText(PROVIDER[i]+"  /  "+v.note);',
'''c.meta.setText("SOURCE  "+PROVIDER[i]+"\n"+v.note);
      c.meta.setContentDescription("Provider "+PROVIDER[i]+". "+v.note);''')
# Distinguish missing values from real zero and make failed values unmistakable.
once('c.figure.setTextColor(error?RED:usable&&!old?WHITE:0xFFB0C4D6);',
'''c.figure.setTextColor(error?RED:usable&&!old?WHITE:0xFFB0C4D6);
      c.figure.setAlpha(usable?1f:.75f);''')
# Ensure live signal animation stops when source changes or page is no longer running.
once('c.dot.animate().cancel();',
'''c.dot.animate().cancel();c.dot.clearAnimation();''')
# Increase title legibility without changing the original layout engine.
once('TextView title=label("  "+NAME[i],11,SECTOR_ACCENT[i],true);',
     'TextView title=label("  "+NAME[i],12,SECTOR_ACCENT[i],true);')
p.write_text(s)
g=root/'app/build.gradle.kts';t=g.read_text()
old='versionName = "1728.2.21.4.47.1"'
if t.count(old)!=1:raise RuntimeError('Expected Build 47.1 source')
g.write_text(t.replace(old,'versionName = "1728.2.21.4.47.2"'))
print('Build 47.2: visible source attribution, updated-age labels, accessible status and improved live tile hierarchy')
