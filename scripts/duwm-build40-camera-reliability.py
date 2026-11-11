from pathlib import Path
import sys
root=Path(sys.argv[1])
java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
cam=java/'Duwm1718MonitorsCamActivity.java'
s=cam.read_text()
def once(a,b):
 global s
 if s.count(a)!=1: raise RuntimeError('Build 40 patch mismatch: '+a[:90])
 s=s.replace(a,b)
# Persist camera exposure and white-balance selection only after the hardware accepts them.
once('p.setExposureCompensation(target);camera.setParameters(p);',
     'p.setExposureCompensation(target);camera.setParameters(p);getSharedPreferences(VIDEO_SETTINGS,MODE_PRIVATE).edit().putInt("last_exposure_compensation",target).apply();')
once('p.setWhiteBalance(next);camera.setParameters(p);selectedWhiteBalance=next;',
     'p.setWhiteBalance(next);camera.setParameters(p);selectedWhiteBalance=next;getSharedPreferences(VIDEO_SETTINGS,MODE_PRIVATE).edit().putString("last_white_balance",next).apply();')
# Make unsupported hardware modes explicit and keep the previous mode state unchanged on failure.
once('nightModeEnabled=!nightModeEnabled;\n            p.setSceneMode(nightModeEnabled?Camera.Parameters.SCENE_MODE_NIGHT:Camera.Parameters.SCENE_MODE_AUTO);\n            camera.setParameters(p);indicator.setText(nightModeEnabled?"● DEVICE NIGHT MODE ON":"● DEVICE NIGHT MODE OFF");',
     'boolean nextNightMode=!nightModeEnabled;\n            p.setSceneMode(nextNightMode?Camera.Parameters.SCENE_MODE_NIGHT:Camera.Parameters.SCENE_MODE_AUTO);\n            camera.setParameters(p);nightModeEnabled=nextNightMode;getSharedPreferences(VIDEO_SETTINGS,MODE_PRIVATE).edit().putBoolean("last_night_mode",nightModeEnabled).apply();indicator.setText(nightModeEnabled?"● DEVICE NIGHT MODE ON":"● DEVICE NIGHT MODE OFF");')
# Surface a non-intrusive recording failure message instead of silently leaving an invalid draft.
once('indicator.setText(valid?"● VIDEO SAVED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");',
     'indicator.setText(valid?"● VIDEO SAVED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");if(!valid)note("Recording could not be finalized. Check storage space and retry.");')
cam.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
old='versionName = "1728.2.21.4.39"'
if v.count(old)!=1: raise RuntimeError('Expected Build 39 version')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.40"'))
print('Build 40: camera settings persistence, safe night-mode state, visible recording failure feedback')
