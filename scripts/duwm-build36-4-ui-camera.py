from pathlib import Path
import sys
root=Path(sys.argv[1])
java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
camera=java/'Duwm1718MonitorsCamActivity.java'
theme=java/'DuwmUnifiedTheme.java'
gradle=root/'app/build.gradle.kts'
s=camera.read_text()
def patch(a,b):
 global s
 if s.count(a)!=1: raise RuntimeError('Build 36.4 patch target not unique: '+a[:75])
 s=s.replace(a,b)
# Accessible, functional recording controls with no changes to recording engine.
patch('recordButton.setMinHeight(dp(62));','recordButton.setMinHeight(dp(68));recordButton.setContentDescription("Start or stop video recording");')
patch('quickGrid=action("GRID",','quickGrid=action("GRID",')
patch('TextView quickTorch=action("LIGHT",this::toggleTorch);','TextView quickTorch=action("LIGHT",this::toggleTorch);quickTorch.setContentDescription("Toggle camera torch when available");')
patch('TextView quickZoom=action("ZOOM +",this::zoomCamera);','TextView quickZoom=action("ZOOM +",this::zoomCamera);quickZoom.setContentDescription("Increase camera zoom when supported");')
patch('TextView quickFocus=action("FOCUS",this::focusOnce);','TextView quickFocus=action("FOCUS",this::focusOnce);quickFocus.setContentDescription("Trigger camera autofocus");')
patch('for(TextView control:new TextView[]{quickGrid,quickTorch,quickZoom,quickFocus}){','quickGrid.setContentDescription("Show or hide composition grid");\n        for(TextView control:new TextView[]{quickGrid,quickTorch,quickZoom,quickFocus}){')
camera.write_text(s)
t=theme.read_text()
needle='    public static final int DEEP_BLUE_ACCENT = 0xFF0D2A45;'
if t.count(needle)!=1: raise RuntimeError('Theme anchor missing')
t=t.replace(needle,needle+'''
    // Build 36.4: one app-wide semantic palette for consistent information states.
    public static final int SIGNAL_AIRCRAFT = 0xFFF57C00;
    public static final int SIGNAL_VESSEL = 0xFF2585D0;
    public static final int SIGNAL_SATELLITE = 0xFFFBC02D;
    public static final int SIGNAL_NEWS = 0xFFAD77D8;
    public static final int SIGNAL_COMMS = 0xFF00BCD4;
    public static final int SIGNAL_NEUTRAL = 0xFFDEE5EF;
    public static final int CARD_HAIRLINE = 0xFF28547A;
''')
theme.write_text(t)
g=gradle.read_text()
old='versionName = "1728.2.21.4.36.3"'
if g.count(old)!=1: raise RuntimeError('Version mismatch')
gradle.write_text(g.replace(old,'versionName = "1728.2.21.4.36.4"'))
print('Applied Build 36.4 camera control and theme source updates')
