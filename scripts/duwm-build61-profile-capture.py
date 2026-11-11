from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 n=s.count(a)
 if n!=1:raise RuntimeError('Build 61 anchor mismatch (%d): %s'%(n,a[:95]))
 s=s.replace(a,b)
# Ensure profile selection is applied again immediately before recording.
once('recordingStartedAtMs=System.currentTimeMillis();lastRecordedMp4=null;',
     'applyLensProfile(getSharedPreferences("duwm_lens_profiles",MODE_PRIVATE).getInt("selected",0));recordingStartedAtMs=System.currentTimeMillis();lastRecordedMp4=null;')
# Keep scene and saturation controls truthful: use only supported hardware parameters.
once('if(effects!=null&&effects.contains(effect))params.setColorEffect(effect);',
'''if(effects!=null&&effects.contains(effect))params.setColorEffect(effect);
            // The six profiles are distinct camera parameter presets, not optical lens emulation.
            int exposureSteps=0;
            switch(selection) {
                case 0: exposureSteps=1; break;  // Clarity: brighter detail
                case 1: exposureSteps=0; break;  // Natural: neutral
                case 2: exposureSteps=0; break;  // Motion: preserve exposure
                case 3: exposureSteps=0; break;  // Balanced: neutral
                case 4: exposureSteps=-1; break; // Cinema: highlight protection
                case 5: exposureSteps=-1; break; // Portrait: highlight protection
            }''')
once('int ev=0;\n            if(selection==4||selection==5)ev=-1;\n            if(selection==0)ev=1;',
     'int ev=exposureSteps;')
# Do not promise changes that cannot be reproduced in encoded footage.
once('note(DUWM_LENS_PROFILES[selection]+" • supported camera controls applied");',
     'note(DUWM_LENS_PROFILES[selection]+" • camera controls active; MP4 colour processing depends on device");')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
old='versionName = "1728.2.21.4.60"'
if v.count(old)!=1:raise RuntimeError('Build 60 version mismatch')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.61"'))
print('Build 61: profile reapply before capture, explicit per-profile exposure and truthful MP4 limitations')
