from pathlib import Path
import sys
root=Path(sys.argv[1])
p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Build 65 anchor mismatch (%d): %s'%(s.count(a),a[:100]))
 s=s.replace(a,b)
# Visible camera upgrade: selected lens displayed on the quick-action control.
once('TextView lensProfileButton=action("LENS PROFILE",this::chooseLensProfile);',
'''int savedLens=getSharedPreferences("duwm_lens_profiles",MODE_PRIVATE).getInt("selected",0);
        TextView lensProfileButton=action("LENS: "+DUWM_LENS_PROFILES[Math.max(0,Math.min(5,savedLens))],this::chooseLensProfile);
        activeLensButton=lensProfileButton;''')
once('private static final String[] DUWM_LENS_PROFILES={',
'''private TextView activeLensButton;
    private static final String[] DUWM_LENS_PROFILES={''')
once('note(DUWM_LENS_PROFILES[selection]+" • camera controls active; MP4 colour processing depends on device");',
'''if(activeLensButton!=null)activeLensButton.setText("LENS: "+DUWM_LENS_PROFILES[selection]);
            note(DUWM_LENS_PROFILES[selection]+" • camera controls active; MP4 colour processing depends on device");''')
# Give each profile a visible, accurate description in the chooser.
once('.setTitle("DUWM • Camera processing profiles")',
     '.setTitle("DUWM • Six lens-style profiles")')
once('private void chooseLensProfile() {',
'''private void chooseLensProfile() {
        // Profile names are lens-inspired software presets, not physical lens replacements.''')
# Distinct export UI feedback for the selected lens.
once('note("Exporting lens-graded MP4; original preserved");',
     'note("Exporting "+DUWM_LENS_PROFILES[Math.max(0,Math.min(5,selected))]+" MP4 • original preserved");')
once('public void success(java.io.File result){runOnUiThread(()->note("Lens MP4 exported: "+result.getName()));}',
     'public void success(java.io.File result){runOnUiThread(()->note("Lens export complete: "+result.getName()+" ("+(result.length()/1024)+" KB)"));}')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text()
old='versionName = "1728.2.21.4.64"'
if v.count(old)!=1:raise RuntimeError('Build 64 version missing')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.65"'))
print('Build 65 initial increment: visible selected lens, live selector updates, export profile feedback and output size')
