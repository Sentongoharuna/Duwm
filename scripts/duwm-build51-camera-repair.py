from pathlib import Path
import sys,re
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def replace_once(old,new,required=True):
 global s
 n=s.count(old)
 if n==1:s=s.replace(old,new)
 elif required:raise RuntimeError(f'Build 51 anchor mismatch ({n}): {old[:100]}')
# Upgrade actual camera display without relying on obsolete Build 50 full-line matches.
replace_once('rec.setColor(0xFFD50000);rec.setCornerRadius(dp(34));rec.setStroke(dp(2),0xFFDEE5EF);',
 'rec.setColor(0xFFF04D5B);rec.setCornerRadius(dp(34));rec.setStroke(dp(2),0xFFF0F5FB);',False)
replace_once('recordButton.setText("■ STOP");',
 'recordButton.setText("■ STOP");recordButton.setContentDescription("Stop recording and save video");',True)
replace_once('unlockInputs();recordButton.setText("● REC");',
 'unlockInputs();recordButton.setText("● REC");recordButton.setContentDescription("Start recording");',True)
# Preserve existing recording/encoding logic; only reformat the visible timer.
old='indicator.setText(String.format(Locale.US,"● REC %d/%ds • %s • VIEW FPS %s / %d target%s",secs,limitSeconds,level,rate,outputFps,quality));'
new='indicator.setText(String.format(Locale.US,"● REC %02d:%02d / %02d:%02d  •  %s  •  FPS %s / %d%s",secs/60,secs%60,limitSeconds/60,limitSeconds%60,level,rate,outputFps,quality));'
replace_once(old,new,False)
# Reliable failure feedback should not claim a video was saved before validation.
replace_once('indicator.setText(valid?"● VIDEO SAVED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");',
 'indicator.setText(valid?"● VIDEO CAPTURED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");',True)
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
old='versionName = "1728.2.21.4.49"'
if v.count(old)!=1:raise RuntimeError('Build 49 version missing')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.51"'))
print('Build 51: repaired camera patch anchors, recording accessibility, visible status and timer where supported')
