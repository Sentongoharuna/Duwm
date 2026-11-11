from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1: raise RuntimeError('Build 55 target mismatch: '+a[:100])
 s=s.replace(a,b)
# Make telemetry labels truly see-through while retaining legible foreground.
once('recordingProfile.setBackgroundColor(android.graphics.Color.TRANSPARENT);',
     'recordingProfile.setBackgroundColor(android.graphics.Color.TRANSPARENT);recordingProfile.setElevation(0f);')
once('indicator.setBackgroundColor(android.graphics.Color.TRANSPARENT);',
     'indicator.setBackgroundColor(android.graphics.Color.TRANSPARENT);indicator.setElevation(0f);indicator.setOnClickListener(v->playRecordedMp4());indicator.setContentDescription("Recording status; tap after capture to review MP4");')
# Confirm the container is actually decodable and includes a video track.
import re
pattern=r'boolean valid=outputFile!=null&&outputFile\\.(?:exists\\(\\)|isFile\\(\\))(?:&&[^;]*)?;'
replacement='boolean valid=outputFile!=null&&outputFile.isFile()&&outputFile.canRead()&&outputFile.length()>4096&&hasPlayableMp4(outputFile);'
s,n=re.subn(pattern,replacement,s)
if n!=1: raise RuntimeError('Build 55 validity anchor not found uniquely: '+str(n))
once('indicator.setText(valid?"● VIDEO CAPTURED / REVIEW IN GALLERY":"● VIDEO ERROR / RETRY");',
     'indicator.setText(valid?"● MP4 READY • TAP TO PLAY":"● MP4 INVALID / RETRY");')
helper="""
    private boolean hasPlayableMp4(java.io.File file) {
        android.media.MediaMetadataRetriever retriever=new android.media.MediaMetadataRetriever();
        try {
            retriever.setDataSource(file.getAbsolutePath());
            String duration=retriever.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_DURATION);
            String width=retriever.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_VIDEO_WIDTH);
            String height=retriever.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_VIDEO_HEIGHT);
            return duration!=null&&Long.parseLong(duration)>0&&width!=null&&Integer.parseInt(width)>0&&height!=null&&Integer.parseInt(height)>0;
        } catch(Exception ex) { android.util.Log.e("DUWM55","MP4 metadata invalid",ex);return false; }
        finally { try {retriever.release();}catch(Exception ignored){} }
    }
    private void playRecordedMp4() {
        if(outputFile==null||!hasPlayableMp4(outputFile)) {
            android.widget.Toast.makeText(this,"No playable MP4 yet. Record and stop first.",android.widget.Toast.LENGTH_LONG).show();return;
        }
        android.widget.VideoView video=new android.widget.VideoView(this);
        video.setVideoURI(android.net.Uri.fromFile(outputFile));
        android.widget.MediaController controls=new android.widget.MediaController(this);
        video.setMediaController(controls);
        android.app.AlertDialog dialog=new android.app.AlertDialog.Builder(this).setTitle("DUWM • MP4 review").setView(video).setPositiveButton("Close",(d,w)->video.stopPlayback()).create();
        dialog.setOnDismissListener(d->video.stopPlayback());
        video.setOnPreparedListener(mp->{video.start();controls.show(2500);});
        video.setOnErrorListener((mp,what,extra)->{android.widget.Toast.makeText(this,"MP4 playback failed ("+what+")",android.widget.Toast.LENGTH_LONG).show();return true;});
        dialog.show();
    }
"""
pos=s.rfind('}')
if pos<0:raise RuntimeError('Camera class closing brace missing')
s=s[:pos]+helper+s[pos:]
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
old='versionName = "1728.2.21.4.54"'
if v.count(old)!=1:raise RuntimeError('Build 54 version not found')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.55"'))
print('Build 55: transparent overlay, MP4 metadata verification, in-app tap-to-play review')
