from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 n=s.count(a)
 if n!=1:raise RuntimeError('Lens profiles anchor mismatch (%d): %s'%(n,a[:90]))
 s=s.replace(a,b)
once('TextView quickFocus=action("FOCUS",this::focusOnce);',
'''TextView quickFocus=action("FOCUS",this::focusOnce);
        TextView lensProfileButton=action("LENS PROFILE",this::chooseLensProfile);
        lensProfileButton.setContentDescription("Select one of six camera processing profiles");''')
once('new TextView[]{quickGrid,quickTorch,quickZoom,quickZoomOut,quickZoomReset,quickFocus,quickEvDown,quickEvUp,quickBalance,quickNight}',
     'new TextView[]{quickGrid,quickTorch,quickZoom,quickZoomOut,quickZoomReset,quickFocus,quickEvDown,quickEvUp,quickBalance,quickNight,lensProfileButton}')
helper="""
    private static final String[] DUWM_LENS_PROFILES={
        "ZEISS Clarity","Leica Natural","Sony Motion","Canon Balanced","ARRI Cinema","Cooke Portrait"
    };
    private void chooseLensProfile() {
        int previous=getSharedPreferences("duwm_lens_profiles",MODE_PRIVATE).getInt("selected",0);
        new android.app.AlertDialog.Builder(this)
            .setTitle("DUWM • Camera processing profiles")
            .setSingleChoiceItems(DUWM_LENS_PROFILES,previous,(dialog,which)->{
                applyLensProfile(which);
                dialog.dismiss();
            }).setNegativeButton("Cancel",null).show();
    }
    private void applyLensProfile(int selection) {
        if(selection<0||selection>=DUWM_LENS_PROFILES.length)return;
        if(camera==null) {
            note("Camera is not ready; profile saved for selection");
            getSharedPreferences("duwm_lens_profiles",MODE_PRIVATE).edit().putInt("selected",selection).apply();
            return;
        }
        try {
            Camera.Parameters params=camera.getParameters();
            java.util.List<String> effects=params.getSupportedColorEffects();
            String effect=Camera.Parameters.EFFECT_NONE;
            // Real hardware capabilities only; avoid falsely simulating cinema glass.
            if(effects!=null&&effects.contains(effect))params.setColorEffect(effect);
            java.util.List<String> balances=params.getSupportedWhiteBalance();
            String balance=Camera.Parameters.WHITE_BALANCE_AUTO;
            if(selection==4||selection==5) {
                if(balances!=null&&balances.contains(Camera.Parameters.WHITE_BALANCE_CLOUDY_DAYLIGHT))
                    balance=Camera.Parameters.WHITE_BALANCE_CLOUDY_DAYLIGHT;
            } else if(selection==0||selection==2) {
                if(balances!=null&&balances.contains(Camera.Parameters.WHITE_BALANCE_DAYLIGHT))
                    balance=Camera.Parameters.WHITE_BALANCE_DAYLIGHT;
            }
            if(balances!=null&&balances.contains(balance))params.setWhiteBalance(balance);
            int ev=0;
            if(selection==4||selection==5)ev=-1;
            if(selection==0)ev=1;
            ev=Math.max(params.getMinExposureCompensation(),Math.min(params.getMaxExposureCompensation(),ev));
            if(params.getExposureCompensationStep()>0)params.setExposureCompensation(ev);
            java.util.List<String> focuses=params.getSupportedFocusModes();
            String desired=selection==2?Camera.Parameters.FOCUS_MODE_CONTINUOUS_VIDEO:Camera.Parameters.FOCUS_MODE_AUTO;
            if(focuses!=null&&focuses.contains(desired))params.setFocusMode(desired);
            camera.setParameters(params);
            getSharedPreferences("duwm_lens_profiles",MODE_PRIVATE).edit().putInt("selected",selection).apply();
            note(DUWM_LENS_PROFILES[selection]+" • supported camera controls applied");
        } catch(RuntimeException ex) {
            android.util.Log.e("DUWM_LENS","Camera rejected profile",ex);
            note("Lens profile unsupported on this camera; previous settings retained");
        }
    }
"""
pos=s.rfind('}')
if pos<0:raise RuntimeError('Camera class terminator missing')
s=s[:pos]+helper+s[pos:]
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
old='versionName = "1728.2.21.4.59"'
if v.count(old)!=1:raise RuntimeError('Build 59 version missing')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.60"'))
print('Build 60: six selectable camera hardware-control profiles with persistence, capability checks and truthful labels')
