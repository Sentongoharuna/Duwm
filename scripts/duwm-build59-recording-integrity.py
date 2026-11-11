from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 n=s.count(a)
 if n!=1:raise RuntimeError(f'Build 59 anchor mismatch ({n}): {a[:90]}')
 s=s.replace(a,b)
# Reject stale MP4 files: capture a timestamp at recording-start button transition.
once('recordButton.setText("■ STOP");recordButton.setContentDescription("Stop recording and save video");',
     'recordingStartedAtMs=System.currentTimeMillis();lastRecordedMp4=null;recordButton.setText("■ STOP");recordButton.setContentDescription("Stop recording and save video");')
once('private java.io.File lastRecordedMp4;',
     'private java.io.File lastRecordedMp4;private long recordingStartedAtMs=0L;')
once('if(candidate.isFile()&&candidate.getName().toLowerCase(java.util.Locale.US).endsWith(".mp4")&&',
     'if(candidate.isFile()&&candidate.canRead()&&candidate.length()>4096&&candidate.lastModified()>=recordingStartedAtMs-2000L&&candidate.getName().toLowerCase(java.util.Locale.US).endsWith(".mp4")&&')
# Prevent stale-file playback even if the recording flag is true.
once('lastRecordedMp4=valid?findLatestRecordedMp4():null;if(valid&&lastRecordedMp4==null)',
     'lastRecordedMp4=valid?findLatestRecordedMp4():null;if(lastRecordedMp4!=null&&!hasPlayableMp4(lastRecordedMp4))lastRecordedMp4=null;if(valid&&lastRecordedMp4==null)')
# Truthful status for a recording that has not yet been located.
once('indicator.setText(valid?"● MP4 SAVED • TAP TO REVIEW":"● RECORDING FAILED • RETRY");',
     'indicator.setText(valid&&lastRecordedMp4!=null?"● MP4 READY • TAP TO REVIEW":valid?"● MP4 NOT LOCATED • CHECK STORAGE":"● RECORDING FAILED • RETRY");')
# Keep playback controls visible on paused video.
once('video.setOnCompletionListener(mp->{video.setKeepScreenOn(false);controls.show(0);});',
     'video.setOnCompletionListener(mp->{video.setKeepScreenOn(false);controls.show(0);});video.setOnInfoListener((mp,what,extra)->{if(what==android.media.MediaPlayer.MEDIA_INFO_VIDEO_RENDERING_START)android.util.Log.i("DUWM59","MP4 first frame rendered");return false;});')
p.write_text(s)
g=root/'app/build.gradle.kts'
v=g.read_text()
old='versionName = "1728.2.21.4.58"'
if v.count(old)!=1:raise RuntimeError('Build 58 version mismatch')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.59"'))
print('Build 59: recording-to-MP4 association, stale-file prevention, playable-file verification, truthful status and playback logging')
