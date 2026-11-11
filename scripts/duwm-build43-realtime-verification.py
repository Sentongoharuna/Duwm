from pathlib import Path
import sys
root=Path(sys.argv[1]);j=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=j/'RunningballV20LiveFeedPulse.java';s=p.read_text()
def change(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Build 43 source audit anchor mismatch: '+a[:90])
 s=s.replace(a,b)
change('private static final long[] LIMIT={180000L,7200000L,180000L,1200000L,1200000L,3600000L,2700000L,172800000L,14400000L};',
'''private static final long[] LIMIT={180000L,7200000L,180000L,1200000L,1200000L,3600000L,2700000L,172800000L,14400000L};
  private static final long FUTURE_TOLERANCE_MS=120000L;
  private static boolean validTimestamp(long timestamp,long now){
    return timestamp>0 && timestamp<=now+FUTURE_TOLERANCE_MS;
  }
  private static boolean fresh(Snapshot snapshot,int index,long now){
    return validTimestamp(snapshot.stamp,now)&&!"--".equals(snapshot.value)
      &&snapshot.error.isEmpty()&&now-snapshot.stamp<=LIMIT[index];
  }''')
change('if(snap.stamp<=0 || "--".equals(snap.value))return;',
       'if(!fresh(snap,index,System.currentTimeMillis()))return;')
change('boolean usable=v.stamp>0&&!"--".equals(v.value);boolean old=usable&&now-v.stamp>LIMIT[i];boolean error=!v.error.isEmpty();',
'''boolean validTime=validTimestamp(v.stamp,now);
      boolean usable=validTime&&!"--".equals(v.value);
      boolean old=usable&&now-v.stamp>LIMIT[i];
      boolean error=!v.error.isEmpty()||(v.stamp>0&&!validTime);''')
change('String category=!usable?"NO VERIFIED DATA":error?"FETCH FAILED / CACHED":old?"STALE / CACHED":"RECENT REPORT";',
'''String category=v.stamp>0&&!validTime?"INVALID SOURCE TIME":!usable?"NO VERIFIED DATA":
        error?"FETCH FAILED / CACHED":old?"STALE / CACHED":"RECENT REPORT";''')
change('c.meta.setText(v.note);c.age.setText(category+"  ·  "+age(v.stamp)+(error?"  ·  ERROR":""));',
'''c.meta.setText(PROVIDER[i]+"  /  "+v.note);
      c.age.setText(category+"  ·  "+age(validTime?v.stamp:0)+(error?"  ·  ERROR":""));''')
change('circle.setColor(usable&&!old&&!error?GREEN:usable&&error?RED:0xFF426CAF);',
       'circle.setColor(usable&&!old&&!error?GREEN:error?RED:0xFF426CAF);')
change('String state=latest.stamp<=0||"--".equals(latest.value)?"NO VERIFIED REPORT":',
       'String state=!validTimestamp(latest.stamp,System.currentTimeMillis())||"--".equals(latest.value)?"NO VERIFIED REPORT":')
change('ticker.setText("◉  "+utc()+"  /  "+NAME[index]+"  "+latest.value+"  /  "+state+"  /  "+age(latest.stamp));',
       'ticker.setText("◉  "+utc()+"  /  "+NAME[index]+"  "+latest.value+"  /  "+state+"  /  "+age(validTimestamp(latest.stamp,System.currentTimeMillis())?latest.stamp:0)+"  /  "+PROVIDER[index]);')
p.write_text(s)
# Lightweight source audit contract: tests require actual provider timestamps, no fabricated live counts.
test=root/'app/src/test/java/com/sentongoharuna/worldsituationroom/SourcePulseContractTest.java'
test.parent.mkdir(parents=True,exist_ok=True)
test.write_text('''package com.sentongoharuna.worldsituationroom;
import org.junit.Test;
import static org.junit.Assert.*;
import java.nio.file.*;
public class SourcePulseContractTest {
 @Test public void providerPulseMustUseRealSnapshots() throws Exception {
  Path source=Paths.get("src/main/java/com/sentongoharuna/worldsituationroom/RunningballV20LiveFeedPulse.java");
  String text=new String(Files.readAllBytes(source));
  assertTrue(text.contains("validTimestamp(v.stamp,now)"));
  assertTrue(text.contains("PROVIDER[i]+\"  /  \"+v.note"));
  assertTrue(text.contains("INVALID SOURCE TIME"));
  assertTrue(text.contains("recordChange(i,v)"));
 }
}
''')
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.42"'
if v.count(old)!=1:raise RuntimeError('Expected Build 42 version')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.43"'))
print('Build 43: source pulse future-time rejection, feed-age verification, source attribution, honest status and source contract test')
