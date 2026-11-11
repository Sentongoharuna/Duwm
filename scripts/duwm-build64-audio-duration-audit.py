from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/DuwmLensVideoExport.java'
s=p.read_text()
def once(a,b):
 global s
 n=s.count(a)
 if n!=1:raise RuntimeError(f'Build 64 anchor mismatch ({n}): {a[:100]}')
 s=s.replace(a,b)
# Check the exported audio stream and duration against the source.
once('if(duration==null||Long.parseLong(duration)<=0||width==null||Integer.parseInt(width)<=0||height==null||Integer.parseInt(height)<=0){',
'''if(duration==null||Long.parseLong(duration)<=0||width==null||Integer.parseInt(width)<=0||height==null||Integer.parseInt(height)<=0){''')
once('callback.success(output);',
'''android.media.MediaMetadataRetriever original=new android.media.MediaMetadataRetriever();
                        try {
                            original.setDataSource(input.getAbsolutePath());
                            String originalDuration=original.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_DURATION);
                            String exportedDuration;
                            String exportedAudio;
                            android.media.MediaMetadataRetriever exported=new android.media.MediaMetadataRetriever();
                            try {
                                exported.setDataSource(output.getAbsolutePath());
                                exportedDuration=exported.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_DURATION);
                                exportedAudio=exported.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_HAS_AUDIO);
                            } finally {try{exported.release();}catch(Exception ignored){}}
                            String originalAudio=original.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_HAS_AUDIO);
                            if(originalDuration!=null&&exportedDuration!=null&&
                               Math.abs(Long.parseLong(originalDuration)-Long.parseLong(exportedDuration))>1000L){
                                callback.failure("Export duration differs from original");return;
                            }
                            if("yes".equalsIgnoreCase(originalAudio)&&!"yes".equalsIgnoreCase(exportedAudio)){
                                callback.failure("Audio track missing from exported MP4");return;
                            }
                        } catch(Exception comparisonError) {
                            callback.failure("Export verification failed: "+comparisonError.getMessage());return;
                        } finally {try{original.release();}catch(Exception ignored){}}
                        callback.success(output);''')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
old='versionName = "1728.2.21.4.63"'
if v.count(old)!=1:raise RuntimeError('Build 63 version mismatch')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.64"'))
print('Build 64: MP4 source/export duration comparison and audio track preservation checks')
