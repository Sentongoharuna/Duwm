from pathlib import Path
import sys,re
root=Path(sys.argv[1])
java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
cam=java/'Duwm1718MonitorsCamActivity.java'
s=cam.read_text()
def once(old,new):
 global s
 if s.count(old)!=1: raise RuntimeError('Build 39 camera anchor mismatch: '+old[:80])
 s=s.replace(old,new)
once('LinearLayout quickActions=new LinearLayout(this);quickActions.setGravity(Gravity.CENTER);','LinearLayout quickActions=new LinearLayout(this);quickActions.setGravity(Gravity.CENTER_VERTICAL);')
once('TextView quickFocus=action("FOCUS",this::focusOnce);','''TextView quickFocus=action("FOCUS",this::focusOnce);
        TextView quickEvDown=action("EV −",()->adjustExposure(-1));
        TextView quickEvUp=action("EV +",()->adjustExposure(1));
        TextView quickBalance=action("WB",this::cycleWhiteBalance);
        TextView quickNight=action("NIGHT",this::toggleNightMode);''')
once('new TextView[]{quickGrid,quickTorch,quickZoom,quickZoomOut,quickZoomReset,quickFocus}','new TextView[]{quickGrid,quickTorch,quickZoom,quickZoomOut,quickZoomReset,quickFocus,quickEvDown,quickEvUp,quickBalance,quickNight}')
once('LinearLayout.LayoutParams q=new LinearLayout.LayoutParams(0,dp(43),1);','LinearLayout.LayoutParams q=new LinearLayout.LayoutParams(dp(78),dp(43));')
once('topControls.addView(quickActions,new LinearLayout.LayoutParams(-1,dp(54)));','''android.widget.HorizontalScrollView quickScroller=new android.widget.HorizontalScrollView(this);
        quickScroller.setHorizontalScrollBarEnabled(false);
        quickScroller.addView(quickActions,new android.widget.HorizontalScrollView.LayoutParams(-2,dp(54)));
        topControls.addView(quickScroller,new LinearLayout.LayoutParams(-1,dp(54)));''')
once('quickGrid.setContentDescription("Show or hide composition grid");','''quickGrid.setContentDescription("Show or hide composition grid");
        quickEvDown.setContentDescription("Decrease device camera exposure");
        quickEvUp.setContentDescription("Increase device camera exposure");
        quickBalance.setContentDescription("Cycle supported white balance modes");
        quickNight.setContentDescription("Toggle supported low-light mode");''')
cam.write_text(s)
p=java/'Duwm1709SectorOutline.java'
t=p.read_text()
for old,new in [('int opacity=selected?206:132;','int opacity=selected?230:178;'),('d.setStroke(width(context),stroke);','d.setStroke(selected?Math.max(2,width(context)):width(context),stroke);')]:
 if t.count(old)!=1: raise RuntimeError('Sector anchor mismatch: '+old)
 t=t.replace(old,new)
colors=['0xFF5CA5F0','0xFF2B9AC9','0xFFCB9462','0xFF7CAFD9','0xFFB69CF0','0xFF55A8B8','0xFF65B7A1','0xFFBD91D6','0xFF8F99E6','0xFF55B2D4','0xFFB191D9','0xFF58B9AE','0xFF9E96E8','0xFFD2B36D','0xFF64C6A3','0xFFE1A18D','0xFF91ACD0','0xFFCE8EA7','0xFFAAC282']
start=t.index('public static final int[] SECTOR_COLORS = {')
end=t.index('};',start)
block=t[start:end]
old_colors=re.findall(r'0xFF[0-9A-Fa-f]{6}',block)
if len(old_colors)!=19: raise RuntimeError('Expected 19 sector colours')
for old,new in zip(old_colors,colors): block=block.replace(old,new,1)
t=t[:start]+block+t[end:]
p.write_text(t)
g=root/'app/build.gradle.kts'
v=g.read_text()
old='versionName = "1728.2.21.4.38"'
if v.count(old)!=1: raise RuntimeError('Expected Build 38 source version')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.39"'))
print('Build 39: scrollable camera hardware controls, 19 category frame accents')
