from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 n=s.count(a)
 if n!=1:raise RuntimeError(f'Build 56 anchor mismatch ({n}): '+a[:90])
 s=s.replace(a,b)
# Review player: attach after dialog is shown, set layout, focus and errors.
once('video.setVideoURI(android.net.Uri.fromFile(lastRecordedMp4));','video.setVideoURI(android.net.Uri.fromFile(lastRecordedMp4));video.setKeepScreenOn(true);video.setFocusable(true);video.setFocusableInTouchMode(true);')
once('video.setMediaController(controls);','video.setMediaController(controls);controls.setAnchorView(video);')
once('dialog.setOnDismissListener(d->video.stopPlayback());','dialog.setOnDismissListener(d->{video.stopPlayback();video.setKeepScreenOn(false);});')
once('video.setOnPreparedListener(mp->{video.start();controls.show(2500);});','video.setOnPreparedListener(mp->{mp.setLooping(false);video.requestFocus();video.start();controls.show(2500);});')
once('dialog.show();','dialog.show();video.setMinimumHeight(dp(240));')
# Validate readable, nonzero duration, actual video dimensions and MP4 format.
once('return duration!=null&&Long.parseLong(duration)>0&&width!=null&&Integer.parseInt(width)>0&&height!=null&&Integer.parseInt(height)>0;',
     'return file.length()>4096&&duration!=null&&Long.parseLong(duration)>0&&width!=null&&Integer.parseInt(width)>0&&height!=null&&Integer.parseInt(height)>0;')
# Surface the true result, never pretend metadata validation guarantees playback or burnt-in overlays.
once('indicator.setText(valid?"● MP4 READY • TAP TO PLAY":"● MP4 INVALID / RETRY");',
     'indicator.setText(valid?"● MP4 CHECKED • TAP TO REVIEW":"● MP4 INVALID • RETRY");')
# Preserve transparent labels, improve contrast through shadow rather than opaque panels.
once('recordingProfile.setBackgroundColor(android.graphics.Color.TRANSPARENT);recordingProfile.setElevation(0f);',
     'recordingProfile.setBackgroundColor(android.graphics.Color.TRANSPARENT);recordingProfile.setElevation(0f);recordingProfile.setShadowLayer(dp(2),0f,dp(1),android.graphics.Color.BLACK);')
once('indicator.setBackgroundColor(android.graphics.Color.TRANSPARENT);indicator.setElevation(0f);',
     'indicator.setBackgroundColor(android.graphics.Color.TRANSPARENT);indicator.setElevation(0f);indicator.setShadowLayer(dp(2),0f,dp(1),android.graphics.Color.BLACK);')
# Versioning only after source edits succeed.
p.write_text(s)
g=root/'app/build.gradle.kts'
v=g.read_text()
once_version='versionName = "1728.2.21.4.55"'
if v.count(once_version)!=1:raise RuntimeError('Build 55 version mismatch')
g.write_text(v.replace(once_version,'versionName = "1728.2.21.4.56"'))
print('Build 56: playback focus, screen awake, controller anchoring, player cleanup, transparent legibility, metadata checks')
