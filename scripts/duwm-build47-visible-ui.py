from pathlib import Path
import sys
root=Path(sys.argv[1]);j=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=j/'RunningballV20LiveFeedPulse.java';s=p.read_text()
def once(a,b):
 global s
 n=s.count(a)
 if n!=1:raise RuntimeError('Build 47 visible UI anchor mismatch '+str(n)+': '+a[:90])
 s=s.replace(a,b)
once('private static final String[] NAME={"AIRCRAFT","SATELLITES","MARITIME","EARTHQUAKES","NASA EVENTS","WORLD NEWS","WEATHER","USD / EUR","SPACE KP"};',
'''private static final String[] NAME={"AIRCRAFT","SATELLITES","MARITIME","EARTHQUAKES","NASA EVENTS","WORLD NEWS","WEATHER","USD / EUR","SPACE KP"};
  private static final int[] SECTOR_ACCENT={0xFF32D7E8,0xFFF4D35E,0xFF4B8FE2,0xFFF04D5B,0xFF9F8BE8,0xFFBE94E5,0xFF39D78A,0xFFF5AD48,0xFF8BC4EF};
  private static int statusColor(boolean usable,boolean old,boolean error){
    return error?RED:!usable?0xFF64839B:old?AMBER:GREEN;
  }''')
once('private static final int BG=0xFF0B1B35, LINE=0xFF284C87, CYAN=0xFF558BDF,',
     'private static final int BG=0xFF071626, LINE=0xFF28547A, CYAN=0xFF32D7E8,')
once('GREEN=0xFF4C78C4, AMBER=DuwmUnifiedTheme.STATUS_ORANGE, RED=DuwmUnifiedTheme.STATUS_RED, DIM=0xFFBBC8CB, WHITE=0xFFE4EDFE;',
     'GREEN=0xFF39D78A, AMBER=DuwmUnifiedTheme.STATUS_ORANGE, RED=DuwmUnifiedTheme.STATUS_RED, DIM=0xFFB0C4D6, WHITE=0xFFF0F5FB;')
once('private GradientDrawable panel(int border){GradientDrawable d=new GradientDrawable(GradientDrawable.Orientation.TL_BR,new int[]{0xFF0D1E3B,BG});d.setStroke(dp(1),border);d.setCornerRadius(dp(13));return d;}',
     'private GradientDrawable panel(int border){GradientDrawable d=new GradientDrawable(GradientDrawable.Orientation.TL_BR,new int[]{0xFF102C46,0xFF0B2035});d.setStroke(dp(1),border);d.setCornerRadius(dp(12));return d;}')
once('box.setPadding(dp(12),dp(10),dp(11),dp(10));box.setBackground(panel(LINE));',
     'box.setPadding(dp(12),dp(12),dp(11),dp(12));box.setBackground(panel(SECTOR_ACCENT[i]));')
once('View dot=new View(getContext());GradientDrawable circle=new GradientDrawable();',
     'View dot=new View(getContext());dot.setAlpha(1f);GradientDrawable circle=new GradientDrawable();')
once('TextView title=label("  "+NAME[i],11,CYAN,true);',
     'TextView title=label("  "+NAME[i],11,SECTOR_ACCENT[i],true);')
once('TextView value=label("--",22,WHITE,true);',
     'TextView value=label("--",24,WHITE,true);')
once('TextView age=label("NOT RECEIVED",9,AMBER,false);',
     'TextView age=label("NOT RECEIVED",10,AMBER,true);')
once('c.age.setTextColor(tint);',
     'c.age.setTextColor(tint);c.figure.setContentDescription(NAME[i]+" "+v.value+" "+category);')
once('circle.setColor(usable&&!old&&!error?GREEN:error?RED:0xFF426CAF);c.dot.setBackground(circle);',
'''circle.setColor(statusColor(usable,old,error));c.dot.setBackground(circle);
      c.dot.animate().cancel();
      if(usable&&!old&&!error&&running){c.dot.setAlpha(1f);c.dot.animate().alpha(.35f).setDuration(900).withEndAction(()->{if(running)c.dot.animate().alpha(1f).setDuration(900).start();}).start();}
      else c.dot.setAlpha(1f);''')
p.write_text(s)
g=root/'app/build.gradle.kts';t=g.read_text();old='versionName = "1728.2.21.4.46"'
if t.count(old)!=1:raise RuntimeError('Build 46 base missing')
g.write_text(t.replace(old,'versionName = "1728.2.21.4.47"'))
print('Build 47: 9 visibly differentiated provider tiles, dark navy cards, large readings, data-driven active light pulse, accessibility')
