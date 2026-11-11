from pathlib import Path
import sys
root=Path(sys.argv[1]);j=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
# Update obsolete contract assertion: 47.2 deliberately changed the visible provider prefix.
test=root/'app/src/test/java/com/sentongoharuna/worldsituationroom/SourcePulseContractTest.java'
s=test.read_text();old='assertTrue(text.contains("PROVIDER[i]+\\\"  /  \\\"+v.note"));'
if s.count(old)!=1:raise RuntimeError('Old source contract assertion not found')
test.write_text(s.replace(old,'assertTrue(text.contains("PROVIDER[i]"));\n  assertTrue(text.contains("SOURCE  "));'))
# Improve the original globe's status hierarchy without moving the original globe or its data.
p=j/'OperationsGlobeView.java';s=p.read_text()
old='private final int OCEAN_COLOR=DuwmUnifiedTheme.MAP_OCEAN, LAND=DuwmUnifiedTheme.MAP_COAST, GRID=Color.argb(58,50,215,232), EDGE=DuwmUnifiedTheme.MAP_RIM;'
new='private final int OCEAN_COLOR=DuwmUnifiedTheme.MAP_OCEAN, LAND=DuwmUnifiedTheme.MAP_COAST, GRID=Color.argb(78,50,215,232), EDGE=DuwmUnifiedTheme.MAP_RIM;'
if s.count(old)!=1:raise RuntimeError('Original globe visual target missing')
p.write_text(s.replace(old,new))
# Make section outlines visible without creating another map.
p=j/'Duwm1709SectorOutline.java';s=p.read_text()
old='int opacity=selected?238:190;'
if s.count(old)!=1:raise RuntimeError('Sector visual target missing')
p.write_text(s.replace(old,'int opacity=selected?248:208;'))
# More readable category titles on the full-screen desk.
p=j/'Duwm1683DeskFullScreenActivity.java';s=p.read_text()
old='TextView name=label(desk.title.toUpperCase(java.util.Locale.US),15,Duwm1709SectorOutline.color(deskIndex),true);'
if s.count(old)!=1:raise RuntimeError('Desk title target missing')
p.write_text(s.replace(old,'TextView name=label(desk.title.toUpperCase(java.util.Locale.US),17,Duwm1709SectorOutline.color(deskIndex),true);'))
g=root/'app/build.gradle.kts';s=g.read_text();old='versionName = "1728.2.21.4.47.3"'
if s.count(old)!=1:raise RuntimeError('Expected 47.3 base')
g.write_text(s.replace(old,'versionName = "1728.2.21.4.48"'))
print('Build 48: repaired obsolete source contract; stronger original globe grid, section outlines and full-screen headings')
