from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/DuwmLensVideoExport.java'
s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Build 63 export anchor mismatch (%d): %s'%(s.count(a),a[:90]))
 s=s.replace(a,b)
once('callback.success(output);', '''if(!output.isFile()||output.length()<4096){
                            callback.failure("Output MP4 is missing or too small");return;
                        }
                        android.media.MediaMetadataRetriever reader=new android.media.MediaMetadataRetriever();
                        try {
                            reader.setDataSource(output.getAbsolutePath());
                            String duration=reader.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_DURATION);
                            String width=reader.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_VIDEO_WIDTH);
                            String height=reader.extractMetadata(android.media.MediaMetadataRetriever.METADATA_KEY_VIDEO_HEIGHT);
                            if(duration==null||Long.parseLong(duration)<=0||width==null||Integer.parseInt(width)<=0||height==null||Integer.parseInt(height)<=0){
                                callback.failure("Exported MP4 has invalid video metadata");return;
                            }
                        } catch(Exception checkError) {
                            callback.failure("Export metadata check failed: "+checkError.getMessage());return;
                        } finally {try{reader.release();}catch(Exception ignored){}}
                        callback.success(output);''')
once('callback.failure(error.getMessage()==null?"Encoding error":error.getMessage());',
     'if(output.exists())output.delete();callback.failure(error.getMessage()==null?"Encoding error":error.getMessage());')
once('} catch(Exception ex) {callback.failure(ex.getMessage()==null?"Could not start export":ex.getMessage());}',
     '} catch(Exception ex) {if(output.exists())output.delete();callback.failure(ex.getMessage()==null?"Could not start export":ex.getMessage());}')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
old='versionName = "1728.2.21.4.62"'
if v.count(old)!=1:raise RuntimeError('Build 62 version mismatch')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.63"'))
print('Build 63: exported MP4 metadata verification, failed export cleanup, original recording preserved')
