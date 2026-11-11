from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Phase 3 camera anchor mismatch '+a[:95])
 s=s.replace(a,b)
once('rec.setColor(0xFFD50000);rec.setCornerRadius(dp(34));rec.setStroke(dp(2),0xFFDEE5EF);',
     'rec.setColor(0xFFF04D5B);rec.setCornerRadius(dp(34));rec.setStroke(dp(2),0xFFF0F5FB);')
once('recordButton.setText("■ STOP");indicator.setText("REC • CLEAN MASTER / AUDIO "+(audioEnabled.isChecked()?"ON":"OFF"));',
'''recordButton.setText("■ STOP");recordButton.setContentDescription("Stop recording and save video");
            recordButton.setBackgroundTintList(android.content.res.ColorStateList.valueOf(0xFFF04D5B));
            indicator.setText("● RECORDING • AUDIO "+(audioEnabled.isChecked()?"ON":"OFF"));indicator.setTextColor(0xFFF0F5FB);''')
once('indicator.setText(String.format(Locale.US,"● REC %d/%ds • %s • VIEW FPS %s / %d target%s",secs,limitSeconds,level,rate,outputFps,quality));',
'''indicator.setText(String.format(Locale.US,"● REC %02d:%02d / %02d:%02d  •  %s  •  FPS %s / %d%s",
                secs/60,secs%60,limitSeconds/60,limitSeconds%60,level,rate,outputFps,quality));
            indicator.setContentDescription("Recording "+secs+" seconds of "+limitSeconds+" seconds. "+level);''')
once('unlockInputs();recordButton.setText("● REC");indicator.setText(valid?"● VIDEO SAVED / PRIVATE DRAFT":"● VIDEO ERROR / RETRY");',
'''unlockInputs();recordButton.setText("● REC");recordButton.setContentDescription("Start recording");
        recordButton.setBackgroundTintList(android.content.res.ColorStateList.valueOf(0xFFF04D5B));
        indicator.setText(valid?"● VIDEO CAPTURED / PROCESSING":"● VIDEO ERROR / RETRY");''')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.49"'
if v.count(old)!=1:raise RuntimeError('Expected Build 49')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.50"'))
print('Build 50 Phase 3: visible recording state, mm:ss timer, clearer mic/FPS feedback, accessible controls and truthful processing status')
