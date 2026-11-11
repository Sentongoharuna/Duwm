from pathlib import Path
import sys
root=Path(sys.argv[1]);j=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=j/'NewsAggregator.java';s=p.read_text()
old='n.publishedAt=i.timestampMs;n.firstSeenAt=System.currentTimeMillis();'
new='''long receivedAt=System.currentTimeMillis();
      // Keep the feed item but never present invalid future timestamps as verified publication dates.
      n.publishedAt=(i.timestampMs>0&&i.timestampMs<=receivedAt+120000L)?i.timestampMs:0L;
      n.firstSeenAt=receivedAt;'''
if s.count(old)!=1:raise RuntimeError('News timestamp patch target mismatch')
p.write_text(s.replace(old,new))
p=j/'NewsSourceHealth.java';s=p.read_text()
old='if(st==State.WORKING&&ok>0&&System.currentTimeMillis()-ok>6L*60L*60L*1000L)st=State.STALE;'
new='''long now=System.currentTimeMillis();
 if(st==State.WORKING&&(ok<=0||ok>now+120000L||now-ok>6L*60L*60L*1000L))st=State.STALE;'''
if s.count(old)!=1:raise RuntimeError('News source health target mismatch')
p.write_text(s.replace(old,new))
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.43"'
if v.count(old)!=1:raise RuntimeError('Build 43 base version mismatch')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.43.2"'))
print('Build 43.2: actual Android news ingestion and source-health timestamps validated')
