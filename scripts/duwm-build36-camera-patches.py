from pathlib import Path
import sys
root=Path(sys.argv[1])
cam=root/"app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java"
gradle=root/"app/build.gradle.kts"
s=cam.read_text()
patches=[
('TextView flip=action("FLIP",this::flipCamera);recordButton=', 'TextView flip=action("FLIP",this::flipCamera);flip.setContentDescription("Switch between front and rear cameras");recordButton='),
('TextView gallery=action("GALLERY",()->{if(!recording)startActivity(new Intent(this,Duwm1726GalleryLibraryActivity.class));});', 'TextView gallery=action("GALLERY",()->{if(!recording)startActivity(new Intent(this,Duwm1726GalleryLibraryActivity.class));});gallery.setContentDescription("Open recorded videos and drafts");'),
('indicator=txt("CAMERA INITIALISING",10);indicator.setSingleLine(true);', 'indicator=txt("CAMERA INITIALISING",10);indicator.setSingleLine(true);indicator.setContentDescription("Camera and recording status");'),
('recordingProfile=txt(profileLabel(),10);recordingProfile.setGravity(Gravity.CENTER);', 'recordingProfile=txt(profileLabel(),10);recordingProfile.setGravity(Gravity.CENTER);recordingProfile.setContentDescription("Selected recording profile");'),
('recordButton.setText("■ STOP");indicator.setText("REC', 'recordButton.setText("■ STOP");recordButton.setContentDescription("Stop recording and save video");recordButton.performHapticFeedback(android.view.HapticFeedbackConstants.CONFIRM);indicator.setText("REC'),
('unlockInputs();recordButton.setText("● REC");indicator.setText(valid?', 'unlockInputs();recordButton.setText("● REC");recordButton.setContentDescription("Start a new video recording");recordButton.performHapticFeedback(android.view.HapticFeedbackConstants.CLOCK_TICK);indicator.setText(valid?'),
('sceneStatus.setTag("scene-ai-status");', 'sceneStatus.setTag("scene-ai-status");sceneStatus.setContentDescription("Scene analysis status. Tap for details");'),
('aspectButton=action(ratioName(),this::switchRatio);qualityButton=action(qualityIndex==0?"HD":"PRO",this::chooseRecordingMode);detailsToggle=action("SETTINGS",this::showCameraSettings);', 'aspectButton=action(ratioName(),this::switchRatio);aspectButton.setContentDescription("Change camera aspect ratio");qualityButton=action(qualityIndex==0?"HD":"PRO",this::chooseRecordingMode);qualityButton.setContentDescription("Choose video recording quality");detailsToggle=action("SETTINGS",this::showCameraSettings);detailsToggle.setContentDescription("Open camera and reporting settings");')
]
for before,after in patches:
    if s.count(before)!=1: raise RuntimeError("Patch target mismatch: "+before[:60])
    s=s.replace(before,after)
cam.write_text(s)
g=gradle.read_text()
if 'versionName = "1728.2.21.4.35"' not in g: raise RuntimeError("Base version mismatch")
gradle.write_text(g.replace('versionName = "1728.2.21.4.35"','versionName = "1728.2.21.4.36"'))
print("Applied 8 Build 36 camera patches")
