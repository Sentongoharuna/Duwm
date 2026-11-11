from pathlib import Path
import sys
root=Path(sys.argv[1]); java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
cam=java/'Duwm1718MonitorsCamActivity.java';s=cam.read_text()
old='if(selected!=null)p.setPreviewFpsRange(selected[0],selected[1]);camera.setParameters(p);'
new='''if(selected!=null)p.setPreviewFpsRange(selected[0],selected[1]);
            // Restore previously selected camera settings, validating each against actual hardware.
            android.content.SharedPreferences savedCamera=getSharedPreferences(VIDEO_SETTINGS,MODE_PRIVATE);
            int savedEv=savedCamera.getInt("last_exposure_compensation",0);
            if(savedEv>=p.getMinExposureCompensation()&&savedEv<=p.getMaxExposureCompensation())p.setExposureCompensation(savedEv);
            String savedBalance=savedCamera.getString("last_white_balance","");
            java.util.List<String> supportedBalances=p.getSupportedWhiteBalance();
            if(supportedBalances!=null&&supportedBalances.contains(savedBalance)){p.setWhiteBalance(savedBalance);selectedWhiteBalance=savedBalance;}
            boolean requestedNight=savedCamera.getBoolean("last_night_mode",false);
            java.util.List<String> supportedScenes=p.getSupportedSceneModes();
            nightModeEnabled=requestedNight&&supportedScenes!=null&&supportedScenes.contains(Camera.Parameters.SCENE_MODE_NIGHT);
            if(nightModeEnabled)p.setSceneMode(Camera.Parameters.SCENE_MODE_NIGHT);
            camera.setParameters(p);'''
if s.count(old)!=1:raise RuntimeError('Build 41 camera restore anchor mismatch')
s=s.replace(old,new)
cam.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.40"'
if v.count(old)!=1:raise RuntimeError('Build 40 version mismatch')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.41"'))
print('Build 41 restores validated camera exposure, white balance and night scene preferences at camera open')
