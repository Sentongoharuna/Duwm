from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(old,new):
 global s
 n=s.count(old)
 if n!=1:raise RuntimeError('Build 57 anchor mismatch (%d): %s'%(n,old[:90]))
 s=s.replace(old,new)
# Keep the preview visible, including while playback controls are dismissed.
once('video.setMinimumHeight(dp(240));','video.setMinimumHeight(dp(320));video.setBackgroundColor(android.graphics.Color.TRANSPARENT);')
# Status text and profile stay transparent with legible, soft shadows.
once('recordingProfile.setShadowLayer(dp(2),0f,dp(1),android.graphics.Color.BLACK);',
     'recordingProfile.setShadowLayer(dp(3),0f,dp(1),0xE6000000);recordingProfile.setTextColor(0xFFF4F8FF);')
once('indicator.setShadowLayer(dp(2),0f,dp(1),android.graphics.Color.BLACK);',
     'indicator.setShadowLayer(dp(3),0f,dp(1),0xE6000000);indicator.setTextColor(0xFFF4F8FF);')
# Replace misleading verification claim with exact metadata-check language.
once('indicator.setText(valid?"● MP4 CHECKED • TAP TO REVIEW":"● MP4 INVALID • RETRY");',
     'indicator.setText(valid?"● MP4 SAVED • TAP TO REVIEW":"● RECORDING FAILED • RETRY");')
# Playback must not leave the display awake after player errors.
once('android.widget.Toast.makeText(this,"MP4 playback failed ("+what+")",android.widget.Toast.LENGTH_LONG).show();return true;',
     'video.setKeepScreenOn(false);android.widget.Toast.makeText(this,"MP4 playback failed ("+what+")",android.widget.Toast.LENGTH_LONG).show();return true;')
p.write_text(s)
g=root/'app/build.gradle.kts'
v=g.read_text()
old='versionName = "1728.2.21.4.56"'
if v.count(old)!=1:raise RuntimeError('Build 56 version mismatch')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.57"'))
print('Build 57: transparent camera labels, contrast, video review sizing, accurate MP4 status, playback cleanup')
