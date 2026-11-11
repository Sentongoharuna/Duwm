from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/RunningballV20LiveFeedPulse.java'
s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Build 47.1 mismatch: '+a[:85])
 s=s.replace(a,b)
once('box.setOnClickListener(v->openDetail(i));',
'''box.setMinimumHeight(dp(112));
    box.setContentDescription(NAME[i]+" intelligence source. Tap to open full details.");
    box.setOnClickListener(v->openDetail(i));''')
once('c.age.setTextColor(tint);c.figure.setContentDescription(NAME[i]+" "+v.value+" "+category);',
'''c.age.setTextColor(tint);c.figure.setContentDescription(NAME[i]+" "+v.value+" "+category);
      c.figure.setTextColor(error?RED:usable&&!old?WHITE:0xFFB0C4D6);
      c.meta.setMaxLines(2);c.meta.setEllipsize(android.text.TextUtils.TruncateAt.END);''')
once('status.setText(recent+" RECENT  /  "+stale+" STALE OR FAILED  /  "+missing+" NOT LOADED  •  NO DEMO COUNTS");',
'''status.setText("● "+recent+" LIVE / VERIFIED    ● "+stale+" DELAYED / FAILED    ● "+missing+" UNAVAILABLE");
    status.setContentDescription(recent+" recent verified sources, "+stale+" delayed or failed, "+missing+" unavailable. No simulated data.");''')
once('ticker.setText("◉  "+utc()+"  /  "+NAME[index]+"  "+latest.value+"  /  "+state+"  /  "+age(validTimestamp(latest.stamp,System.currentTimeMillis())?latest.stamp:0)+"  /  "+PROVIDER[index]);',
'''ticker.setText("◉ "+utc()+"   •   "+NAME[index]+"   "+latest.value+"   •   "+state+"   •   "+age(validTimestamp(latest.stamp,System.currentTimeMillis())?latest.stamp:0)+"   •   "+PROVIDER[index]);
    ticker.setContentDescription(NAME[index]+" "+state+" "+latest.value);''')
p.write_text(s)
g=root/'app/build.gradle.kts';t=g.read_text();old='versionName = "1728.2.21.4.47"'
if t.count(old)!=1:raise RuntimeError('Expected Build 47')
g.write_text(t.replace(old,'versionName = "1728.2.21.4.47.1"'))
print('Build 47.1: visible source counters, high-contrast readings, accessible cards, readable ticker')
