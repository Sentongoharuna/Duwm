from pathlib import Path
import sys
root=Path(sys.argv[1])
java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=java/'Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def replace_one(a,b):
 global s
 n=s.count(a)
 if n!=1: raise RuntimeError(f'Build 37 expected one match, got {n}: {a[:90]}')
 s=s.replace(a,b)
# New zoom-out and reset controls, not just labels. Camera hardware availability checked.
anchor='TextView quickFocus=action("FOCUS",this::focusOnce);'
replace_one(anchor,anchor+'''
        TextView quickZoomOut=action("ZOOM −",()->adjustZoom(-1));
        TextView quickZoomReset=action("1×",()->resetZoom());''')
replace_one('new TextView[]{quickGrid,quickTorch,quickZoom,quickFocus}',
            'new TextView[]{quickGrid,quickTorch,quickZoom,quickZoomOut,quickZoomReset,quickFocus}')
replace_one('control.setTextSize(10);LinearLayout.LayoutParams q=',
            'control.setTextSize(10);control.setContentDescription("Camera control: "+control.getText());LinearLayout.LayoutParams q=')
# Reduce zoom in/out in supported hardware steps, with a separate 1x reset.
anchor='    private void zoomCamera(){'
if s.count(anchor)!=1: raise RuntimeError('Zoom function anchor missing')
s=s.replace(anchor,'''    private void adjustZoom(int direction){
        if(recording||camera==null){note("Zoom unavailable while recording or camera is closed");return;}
        try{
            Camera.Parameters parameters=camera.getParameters();
            if(!parameters.isZoomSupported()){note("This camera does not support zoom");return;}
            int step=Math.max(1,parameters.getMaxZoom()/12);
            int target=Math.max(0,Math.min(parameters.getMaxZoom(),parameters.getZoom()+direction*step));
            parameters.setZoom(target);camera.setParameters(parameters);
            note("Zoom "+target+" / "+parameters.getMaxZoom());
        }catch(Exception error){note("Unable to adjust zoom");}
    }
    private void resetZoom(){
        if(recording||camera==null){note("Stop recording to reset zoom");return;}
        try{
            Camera.Parameters parameters=camera.getParameters();
            if(!parameters.isZoomSupported()){note("Zoom not supported");return;}
            parameters.setZoom(0);camera.setParameters(parameters);note("Zoom reset to 1×");
        }catch(Exception error){note("Unable to reset zoom");}
    }
''' + anchor)
# Avoid controls with insufficient width on narrow screens.
replace_one('control.setTextSize(10);control.setContentDescription','control.setTextSize(9);control.setContentDescription')
p.write_text(s)
# Semantic category colours can be reused by every screen without inventing live status.
t=java/'DuwmUnifiedTheme.java';theme=t.read_text()
anchor='    public static final int CARD_HAIRLINE = 0xFF28547A;'
if theme.count(anchor)!=1: raise RuntimeError('Build 36.4 theme missing')
theme=theme.replace(anchor,anchor+'''
    public static int categoryAccent(String category){
        if(category==null)return SIGNAL_NEUTRAL;
        String key=category.trim().toLowerCase(java.util.Locale.ROOT);
        if(key.contains("aircraft")||key.contains("flight"))return SIGNAL_AIRCRAFT;
        if(key.contains("vessel")||key.contains("ship")||key.contains("marine"))return SIGNAL_VESSEL;
        if(key.contains("satellite")||key.contains("orbit"))return SIGNAL_SATELLITE;
        if(key.contains("news")||key.contains("intelligence"))return SIGNAL_NEWS;
        if(key.contains("radio")||key.contains("tv")||key.contains("network"))return SIGNAL_COMMS;
        return SIGNAL_NEUTRAL;
    }
''')
t.write_text(theme)
g=root/'app/build.gradle.kts';gradle=g.read_text()
old='versionName = "1728.2.21.4.36.5"'
if gradle.count(old)!=1: raise RuntimeError('Expected Build 36.5 version')
g.write_text(gradle.replace(old,'versionName = "1728.2.21.4.37"'))
print('Build 37: zoom-out, 1x reset, camera toolbar layout and shared category accent API applied')
