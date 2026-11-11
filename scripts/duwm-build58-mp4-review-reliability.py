from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 n=s.count(a)
 if n!=1:raise RuntimeError(f'Build 58 anchor mismatch ({n}): '+a[:85])
 s=s.replace(a,b)
# Ensure the preview review surface scales to the available space.
once('video.setMinimumHeight(dp(320));video.setBackgroundColor(android.graphics.Color.TRANSPARENT);',
     'video.setMinimumHeight(dp(320));video.setBackgroundColor(android.graphics.Color.BLACK);video.setZOrderOnTop(false);')
# Show recording duration and resolution in playback title after validation.
once('dialog.show();video.setMinimumHeight(dp(320));',
     'dialog.show();video.setMinimumHeight(dp(320));dialog.getWindow().setSoftInputMode(android.view.WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);')
# Prevent old recordings being silently selected after a new recording fails.
once('lastRecordedMp4=valid?findLatestRecordedMp4():null;',
     'lastRecordedMp4=valid?findLatestRecordedMp4():null;if(valid&&lastRecordedMp4==null)android.util.Log.w("DUWM58","Recording finalized but private MP4 not located");')
# Add media controls and avoid misleading success after missing file.
once('if(lastRecordedMp4==null||!hasPlayableMp4(lastRecordedMp4)) {',
     'if(lastRecordedMp4==null||!lastRecordedMp4.isFile()||!lastRecordedMp4.canRead()||!hasPlayableMp4(lastRecordedMp4)) {')
# Keep playback stable when focus is lost.
once('dialog.setOnDismissListener(d->{video.stopPlayback();video.setKeepScreenOn(false);});',
     'dialog.setOnDismissListener(d->{video.stopPlayback();video.setKeepScreenOn(false);video.suspend();});')
# Explicitly handle end of playback.
once('video.setOnPreparedListener(mp->{mp.setLooping(false);video.requestFocus();video.start();controls.show(2500);});',
     'video.setOnPreparedListener(mp->{mp.setLooping(false);video.requestFocus();video.start();controls.show(2500);});video.setOnCompletionListener(mp->{video.setKeepScreenOn(false);controls.show(0);});')
p.write_text(s)
g=root/'app/build.gradle.kts'
v=g.read_text()
old='versionName = "1728.2.21.4.57"'
if v.count(old)!=1:raise RuntimeError('Build 57 version mismatch')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.58"'))
print('Build 58: MP4 playback lifecycle, completion, missing-file warnings, review layout and media checks')
