from pathlib import Path
import sys
root=Path(sys.argv[1])
cam=root/"app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java"
s=cam.read_text()
def change(a,b):
 global s
 if s.count(a)!=1: raise RuntimeError("Build 36.5 patch target mismatch: "+a[:90])
 s=s.replace(a,b)
# Persistent grid preference shared between quick toolbar and advanced camera settings.
change('private View previewGrid; private boolean showGrid=false;',
       'private View previewGrid; private boolean showGrid=false;\n    private void toggleCompositionGrid(){showGrid=!showGrid;getSharedPreferences(VIDEO_SETTINGS,MODE_PRIVATE).edit().putBoolean("composition_grid_enabled",showGrid).apply();if(previewGrid!=null)previewGrid.invalidate();note(showGrid?"Composition grid enabled":"Composition grid hidden");}')
change('showGrid=!showGrid;if(previewGrid!=null)previewGrid.invalidate();',
       'toggleCompositionGrid();')
# Replace only the quick toolbar handler if it survived the earlier substitution.
s=s.replace('showGrid=!showGrid;if(previewGrid!=null)previewGrid.invalidate();note(showGrid?"Composition grid enabled":"Composition grid hidden");','toggleCompositionGrid();')
# Make recording controls convey state to screen readers and prevent accidental double taps.
change('recordButton.setMinHeight(dp(68));recordButton.setContentDescription("Start or stop video recording");',
       'recordButton.setMinHeight(dp(68));recordButton.setContentDescription("Start or stop video recording");recordButton.setFocusable(true);')
# Improve zoom button: visible zoom feedback even when no gesture is used.
change('camera.setParameters(p);}catch(Exception e){note("Zoom unavailable");}}',
       'camera.setParameters(p);note("Zoom "+p.getZoom()+" / "+p.getMaxZoom());}catch(Exception e){note("Zoom unavailable");}}')
cam.write_text(s)
g=root/"app/build.gradle.kts";t=g.read_text()
old='versionName = "1728.2.21.4.36.4"'
if t.count(old)!=1: raise RuntimeError("Expected 36.4 base version")
g.write_text(t.replace(old,'versionName = "1728.2.21.4.36.5"'))
print("Build 36.5 camera changes applied")
