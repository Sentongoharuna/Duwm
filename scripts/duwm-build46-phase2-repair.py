from pathlib import Path
import sys
root=Path(sys.argv[1]);j=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=j/'RunningballV20LiveFeedPulse.java';s=p.read_text()
def one(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Phase 2 feed target mismatch: '+a[:100])
 s=s.replace(a,b)
one('if(s.stamp>0&&count>=0)s.value=String.valueOf(count);s.error=p("rb19_bootstrap").getString("sat_error","");',
'''if(s.stamp>0&&count>=0)s.value=String.valueOf(count);s.error=p("rb19_bootstrap").getString("sat_error","");
      s.note="CELESTRAK / STATIONS / "+(count>=0?"ORBITAL RECORDS":"NO VALID ORBITAL RECORDS");''')
one('if(s.stamp>0&&count>=0)s.value=String.valueOf(count);if(a.getString("endpoint","").trim().isEmpty()){s.stamp=0;s.note="AIS GATEWAY REQUIRED";}',
'''if(s.stamp>0&&count>=0)s.value=String.valueOf(count);
      if(a.getString("endpoint","").trim().isEmpty()){
        s.stamp=0;s.value="--";s.note="AIS GATEWAY REQUIRED";s.error="NO AUTHORIZED AIS PROVIDER";
      }else{s.note="AIS GATEWAY / "+(count>=0?"RECEIVED ROWS":"NO VERIFIED ROWS");}''')
one('if(i==5){int n=number(o,"articles");if(s.stamp>0&&n>=0)s.value=String.valueOf(n);s.note="RETURNED ARTICLES • NOT GLOBAL TOTAL";}',
'''if(i==5){int n=number(o,"articles");if(s.stamp>0&&n>=0)s.value=String.valueOf(n);
        s.note="GDELT / RETURNED ARTICLES • NOT GLOBAL TOTAL";}''')
one('else{double temp=o.optDouble("temperature",Double.NaN);if(s.stamp>0&&valid(temp))s.value=String.format(Locale.US,"%.1f°C",temp);}',
'''else{double temp=o.optDouble("temperature",Double.NaN);
          if(s.stamp>0&&valid(temp)&&temp>=-100&&temp<=70)s.value=String.format(Locale.US,"%.1f°C",temp);
          else{s.value="--";s.error="INVALID WEATHER TEMPERATURE";}
          s.note="OPEN-METEO / "+RunningballWorldTarget.label(ctx);}''')
p.write_text(s)
# Correct misleading label for the aircraft feed without replacing its existing region-based source.
one('"ADSB.LOL / SELECTED 250 NM"','"ADSB.LOL / SELECTED REGION"')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.45"'
if v.count(old)!=1:raise RuntimeError('Expected Build 45 source version')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.46"'))
print('Build 46 Phase 2: honest AIS unavailable state, satellite source label, weather sanity checks, news provider attribution')
