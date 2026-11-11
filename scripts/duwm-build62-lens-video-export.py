from pathlib import Path
import sys
root=Path(sys.argv[1])
java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=java/'Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError(f'Build 62 anchor mismatch ({s.count(a)}): {a[:100]}')
 s=s.replace(a,b)
# Add a non-destructive export control to the existing MP4 review dialog.
once('.setPositiveButton("Close",(d,w)->video.stopPlayback()).create();',
     '.setNeutralButton("Export Lens Grade",(d,w)->exportLensGrade()).setPositiveButton("Close",(d,w)->video.stopPlayback()).create();')
helper="""
    private void exportLensGrade() {
        if(lastRecordedMp4==null||!lastRecordedMp4.isFile()||!hasPlayableMp4(lastRecordedMp4)){
            note("No valid MP4 available for lens grading");return;
        }
        int selected=getSharedPreferences("duwm_lens_profiles",MODE_PRIVATE).getInt("selected",0);
        java.io.File source=lastRecordedMp4;
        java.io.File dest=new java.io.File(source.getParentFile(),
            source.getName().replaceFirst("(?i)\\\\.mp4$","")+"-lens-"+selected+"-"+System.currentTimeMillis()+".mp4");
        note("Exporting lens-graded MP4; original preserved");
        DuwmLensVideoExport.export(this,source,dest,selected,new DuwmLensVideoExport.Callback(){
            public void success(java.io.File result){runOnUiThread(()->note("Lens MP4 exported: "+result.getName()));}
            public void failure(String message){runOnUiThread(()->note("Lens export failed: "+message));}
        });
    }
"""
pos=s.rfind('}')
s=s[:pos]+helper+s[pos:]
p.write_text(s)
processor=r'''package com.sentongoharuna.worldsituationroom;

import android.content.Context;
import android.net.Uri;
import androidx.media3.common.MediaItem;
import androidx.media3.common.Effect;
import androidx.media3.common.util.UnstableApi;
import androidx.media3.effect.RgbMatrix;
import androidx.media3.transformer.EditedMediaItem;
import androidx.media3.transformer.Effects;
import androidx.media3.transformer.Transformer;
import androidx.media3.transformer.Composition;
import androidx.media3.transformer.ExportResult;
import androidx.media3.transformer.ExportException;
import java.io.File;
import java.util.Collections;
import java.util.concurrent.Executor;

@UnstableApi
public final class DuwmLensVideoExport {
    public interface Callback {void success(File result);void failure(String message);}
    private DuwmLensVideoExport(){}
    public static void export(Context context, File input, File output, int selected, Callback callback){
        try {
            final int profile=Math.max(0,Math.min(5,selected));
            RgbMatrix matrix=new RgbMatrix(){
                @Override public float[] getMatrix(long presentationTimeUs, boolean useHdr){
                    float[][] gains={
                        {1.04f,1.04f,1.04f}, // ZEISS: neutral clarity
                        {1.03f,1.00f,0.98f}, // Leica: natural warmth
                        {1.02f,1.02f,1.03f}, // Sony: cool neutral
                        {1.00f,1.00f,1.00f}, // Canon: neutral
                        {1.05f,1.00f,0.94f}, // ARRI: warm
                        {1.08f,0.99f,0.91f}  // Cooke: warm portrait
                    };
                    float[] g=gains[profile];
                    return new float[]{g[0],0,0,0,0,g[1],0,0,0,0,g[2],0,0,0,0,1};
                }
            };
            Effects effects=new Effects(Collections.emptyList(),Collections.<Effect>singletonList(matrix));
            EditedMediaItem edited=new EditedMediaItem.Builder(MediaItem.fromUri(Uri.fromFile(input)))
                .setEffects(effects).build();
            Transformer transformer=new Transformer.Builder(context)
                .addListener(new Transformer.Listener(){
                    @Override public void onCompleted(Composition composition, ExportResult result){
                        callback.success(output);
                    }
                    @Override public void onError(Composition composition, ExportResult result, ExportException error){
                        callback.failure(error.getMessage()==null?"Encoding error":error.getMessage());
                    }
                }).build();
            transformer.start(edited,output.getAbsolutePath());
        } catch(Exception ex) {callback.failure(ex.getMessage()==null?"Could not start export":ex.getMessage());}
    }
}
'''
(java/'DuwmLensVideoExport.java').write_text(processor)
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
if 'versionName = "1728.2.21.4.61"' not in v:raise RuntimeError('Build 61 version missing')
v=v.replace('versionName = "1728.2.21.4.61"','versionName = "1728.2.21.4.62"')
anchor='dependencies {'
if v.count(anchor)!=1:raise RuntimeError('Gradle dependencies anchor mismatch')
v=v.replace(anchor,anchor+'''
    implementation("androidx.media3:media3-transformer:1.5.1")
    implementation("androidx.media3:media3-effect:1.5.1")
    implementation("androidx.media3:media3-common:1.5.1")
''')
g.write_text(v)
print('Build 62: non-destructive six-profile MP4 RGB export via Media3 Transformer, source recording preserved')
