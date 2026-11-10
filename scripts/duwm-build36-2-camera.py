from pathlib import Path
import sys
root=Path(sys.argv[1]); p=root/"app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java"
s=p.read_text()
def change(a,b):
 global s
 if s.count(a)!=1: raise RuntimeError("Patch mismatch: "+a[:60])
 s=s.replace(a,b)
change("for(TextView t:new TextView[]{aspectButton,qualityButton,detailsToggle}){LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,dp(42),1);lp.setMargins(dp(3),0,dp(3),0);tools.addView(t,lp);}page.addView(tools);","for(TextView t:new TextView[]{aspectButton,qualityButton,detailsToggle}){LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(0,dp(42),1);lp.setMargins(dp(3),0,dp(3),0);tools.addView(t,lp);}page.addView(tools);\n        LinearLayout quickActions=new LinearLayout(this);quickActions.setGravity(Gravity.CENTER);quickActions.setPadding(dp(8),dp(3),dp(8),dp(3));\n        TextView quickGrid=action(\"GRID\",()->{showGrid=!showGrid;if(previewGrid!=null)previewGrid.invalidate();note(showGrid?\"Composition grid enabled\":\"Composition grid hidden\");});\n        TextView quickTorch=action(\"LIGHT\",this::toggleTorch);\n        TextView quickZoom=action(\"ZOOM +\",this::zoomCamera);\n        TextView quickFocus=action(\"FOCUS\",this::focusOnce);\n        for(TextView control:new TextView[]{quickGrid,quickTorch,quickZoom,quickFocus}){\n            control.setTextSize(10);LinearLayout.LayoutParams q=new LinearLayout.LayoutParams(0,dp(43),1);q.setMargins(dp(2),0,dp(2),0);quickActions.addView(control,q);\n        }")
change("topControls.addView(tools,new LinearLayout.LayoutParams(-1,dp(46)));","topControls.addView(tools,new LinearLayout.LayoutParams(-1,dp(46)));\n        topControls.addView(quickActions,new LinearLayout.LayoutParams(-1,dp(49)));")
change("private TextView action(String label,Runnable a){TextView t=txt(label,12);t.setGravity(Gravity.CENTER);t.setBackground(outline());t.setMinHeight(dp(48));t.setOnClickListener(v->a.run());return t;}","private TextView action(String label,Runnable a){TextView t=txt(label,12);t.setGravity(Gravity.CENTER);t.setBackground(outline());t.setMinHeight(dp(48));t.setClickable(true);t.setFocusable(true);t.setOnClickListener(v->a.run());return t;}")
change("recordButton.setTextSize(19);recordButton.setTypeface(Typeface.create(\"sans-serif\",Typeface.BOLD));","recordButton.setTextSize(19);recordButton.setTypeface(Typeface.create(\"sans-serif\",Typeface.BOLD));recordButton.setMinHeight(dp(62));")
change("indicator.setAccessibilityLiveRegion(View.ACCESSIBILITY_LIVE_REGION_POLITE);indicator.setPadding(dp(9),0,dp(9),0);","indicator.setAccessibilityLiveRegion(View.ACCESSIBILITY_LIVE_REGION_POLITE);indicator.setEllipsize(android.text.TextUtils.TruncateAt.END);indicator.setPadding(dp(9),0,dp(9),0);")
change("TextView gallery=action(\"GALLERY\",()->{if(!recording)startActivity(new Intent(this,Duwm1726GalleryLibraryActivity.class));});","TextView gallery=action(\"GALLERY\",()->{if(recording){note(\"Stop recording before opening the gallery\");return;}startActivity(new Intent(this,Duwm1726GalleryLibraryActivity.class));});")
change("private void flipCamera(){if(recording)return;","private void flipCamera(){if(recording){note(\"Stop recording before switching cameras\");return;}")
change("private void zoomCamera(){if(recording||camera==null)return;","private void zoomCamera(){if(recording){note(\"Zoom is locked while recording\");return;}if(camera==null){note(\"Camera not ready\");return;}")
change("private void toggleTorch(){\n        if(recording||camera==null){note(\"Torch cannot change while recording on this camera engine\");return;}","private void toggleTorch(){\n        if(recording||camera==null){note(\"Torch cannot change while recording or while camera is unavailable\");return;}")
p.write_text(s)
g=root/"app/build.gradle.kts";t=g.read_text();old='versionName = "1728.2.21.4.36.1"'
if old not in t: raise RuntimeError("Version mismatch")
g.write_text(t.replace(old,'versionName = "1728.2.21.4.36.2"'))
print("Build 36.2 camera controls applied")
