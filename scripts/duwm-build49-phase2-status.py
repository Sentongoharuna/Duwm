from pathlib import Path
import sys
root=Path(sys.argv[1]);j=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=j/'RunningballV20LiveFeedPulse.java';s=p.read_text()
def one(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Build 49 source target mismatch: '+a[:100])
 s=s.replace(a,b)
# Data age must be checked before declaring any feed current, including future-dated reports.
one('boolean old=usable&&now-v.stamp>LIMIT[i];',
'''boolean old=usable&&(now-v.stamp>LIMIT[i]);''')
one('String category=v.stamp>0&&!validTime?"INVALID SOURCE TIME":!usable?"NO VERIFIED DATA":',
'''String category=v.stamp>0&&!validTime?"INVALID SOURCE TIME":!usable?"NO VERIFIED DATA":''')
# Distinguish an actual unavailable AIS gateway from a stale cached vessel count.
one('c.meta.setText("SOURCE  "+PROVIDER[i]+"\\n"+v.note);',
'''c.meta.setText("SOURCE  "+PROVIDER[i]+"\\n"+v.note);
      if(i==2&&v.error.contains("NO AUTHORIZED AIS PROVIDER"))
        c.meta.setText("VESSEL TRACKING UNAVAILABLE\\nConnect an authorized AIS gateway");''')
# Prevent stale/failed readings from visually looking live; expose a meaningful provider state.
one('c.figure.setAlpha(usable?1f:.75f);',
'''c.figure.setAlpha(usable&&!old&&!error?1f:.70f);
      c.figure.setContentDescription(NAME[i]+" "+v.value+"; "+category+"; "+PROVIDER[i]);''')
one('c.age.setText(category+"  ·  UPDATED "+age(validTime?v.stamp:0)+(error?"  ·  ERROR":""));',
'''c.age.setText(category+"  ·  UPDATED "+age(validTime?v.stamp:0)+(error?"  ·  ERROR":""));
      c.age.setAlpha(error?1f:old?.9f:1f);''')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.48"'
if v.count(old)!=1:raise RuntimeError('Build 48 version missing')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.49"'))
print('Build 49: live data tile freshness, explicit AIS unavailable state and accessibility')
