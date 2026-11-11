from pathlib import Path
import sys
root=Path(sys.argv[1])
java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
camera=java/'Duwm1718MonitorsCamActivity.java'
s=camera.read_text()
def once(old,new):
 global s
 count=s.count(old)
 if count!=1: raise RuntimeError(f'UI polish anchor mismatch ({count}): {old[:70]}')
 s=s.replace(old,new)
# Visually clearer and more touch-friendly camera controls, without changing the camera engine.
once('control.setTextSize(9);control.setContentDescription("Camera control: "+control.getText());',
     'control.setTextSize(11);control.setTypeface(Typeface.create("sans-serif-medium",Typeface.NORMAL));control.setContentDescription("Camera control: "+control.getText());')
once('quickActions.setPadding(dp(8),dp(3),dp(8),dp(3));',
     'quickActions.setPadding(dp(5),dp(5),dp(5),dp(5));')
once('q.setMargins(dp(2),0,dp(2),0);quickActions.addView(control,q);',
     'q.setMargins(dp(3),dp(2),dp(3),dp(2));quickActions.addView(control,q);')
once('topControls.addView(quickActions,new LinearLayout.LayoutParams(-1,dp(49)));',
     'topControls.addView(quickActions,new LinearLayout.LayoutParams(-1,dp(54)));')
camera.write_text(s)
theme=java/'DuwmUnifiedTheme.java'
t=theme.read_text()
anchor='    public static int categoryAccent(String category){'
if t.count(anchor)!=1: raise RuntimeError('Build 37 theme anchor missing')
t=t.replace(anchor,'''    // Shared styling dimensions used by the command-centre interface.
    public static final int HAIRLINE_DP = 1;
    public static final int CARD_CORNER_DP = 12;
    public static final int CARD_INSET_DP = 12;
    public static final int TOUCH_TARGET_DP = 48;
    public static final int NIGHT_BACKGROUND = 0xFF071626;
    public static final int NIGHT_PANEL = 0xFF0B2035;
    public static final int NIGHT_SURFACE = 0xFF102C46;
    public static final int TEXT_PRIMARY = 0xFFF0F5FB;
    public static final int TEXT_SECONDARY = 0xFFB0C4D6;
    public static final int SIGNAL_ALERT = 0xFFE84853;
    public static final int SIGNAL_VERIFIED = 0xFF37C983;
    '''+anchor)
theme.write_text(t)
g=root/'app/build.gradle.kts';b=g.read_text()
old='versionName = "1728.2.21.4.37"'
if b.count(old)!=1: raise RuntimeError('Build 37 version missing')
g.write_text(b.replace(old,'versionName = "1728.2.21.4.37.1"'))
print('Build 37.1: camera toolbar layout refined and dark-navy shared design tokens added')
