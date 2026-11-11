from pathlib import Path
import sys
root=Path(sys.argv[1])
j=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
theme=j/'DuwmUnifiedTheme.java';s=theme.read_text()
changes={
'BACKGROUND = 0xFF041424':'BACKGROUND = 0xFF071626',
'APPROVED_NAVY = 0xFF041424':'APPROVED_NAVY = 0xFF071626',
'OVERLAY = 0xF2041424':'OVERLAY = 0xF2071626',
'MAP_OCEAN = 0xFF051526':'MAP_OCEAN = 0xFF071A2C',
'MAP_OCEAN_SHADE = 0xFF041221':'MAP_OCEAN_SHADE = 0xFF051220',
'MAP_LAND = 0xFF061728':'MAP_LAND = 0xFF0C2C42',
'ACCENT = 0xFFDEE5EF':'ACCENT = 0xFFB0C4D6',
'ACCENT_BRIGHT = 0xFFF5F7FA':'ACCENT_BRIGHT = 0xFFF0F5FB',
'TEXT = 0xFFF5F7FA':'TEXT = 0xFFF0F5FB',
'LIVE = 0xFF00C853':'LIVE = 0xFF39D78A',
'WARNING = 0xFFFBC02D':'WARNING = 0xFFF5AD48',
'DANGER = 0xFFD50000':'DANGER = 0xFFF04D5B',
'STATUS_RED = 0xFFD50000':'STATUS_RED = 0xFFF04D5B',
'STATUS_ORANGE = 0xFFF57C00':'STATUS_ORANGE = 0xFFF5AD48',
'STATUS_YELLOW = 0xFFFBC02D':'STATUS_YELLOW = 0xFFF4D35E',
'STATUS_BLUE = 0xFF0D47A1':'STATUS_BLUE = 0xFF4B8FE2',
'STATUS_CYAN = 0xFF00ACC1':'STATUS_CYAN = 0xFF32D7E8',
'STATUS_GREEN = 0xFF00C853':'STATUS_GREEN = 0xFF39D78A',
'DEEP_BLUE_ACCENT = 0xFF0D2A45':'DEEP_BLUE_ACCENT = 0xFF153B59'
}
for old,new in changes.items():
 if s.count(old)!=1:raise RuntimeError('Build 42 theme mismatch '+old)
 s=s.replace(old,new)
# Already-upgraded theme constants from Build 38 remain the single source for panels and maps.
theme.write_text(s)
sector=j/'Duwm1709SectorOutline.java';t=sector.read_text()
changes={
'int opacity=selected?230:178;':'int opacity=selected?238:190;',
'd.setStroke(selected?Math.max(2,width(context)):width(context),stroke);':'d.setStroke(selected?Math.max(2,width(context)):width(context),stroke);',
'Color.argb(145,Color.red(c),Color.green(c),Color.blue(c))':'Color.argb(184,Color.red(c),Color.green(c),Color.blue(c))'
}
for old,new in changes.items():
 if old==new:continue
 if t.count(old)!=1:raise RuntimeError('Build 42 sector mismatch '+old)
 t=t.replace(old,new)
sector.write_text(t)
# Improve actual original globe palette; do not create a second globe or change data logic.
globe=j/'OperationsGlobeView.java';g=globe.read_text()
old='private final int OCEAN_COLOR=Color.rgb(4,21,43), LAND=DuwmUnifiedTheme.MAP_COAST, GRID=Color.argb(62,57,181,195), EDGE=DuwmUnifiedTheme.MAP_RIM;'
new='private final int OCEAN_COLOR=DuwmUnifiedTheme.MAP_OCEAN, LAND=DuwmUnifiedTheme.MAP_COAST, GRID=Color.argb(58,50,215,232), EDGE=DuwmUnifiedTheme.MAP_RIM;'
if g.count(old)!=1:raise RuntimeError('Build 42 original globe mismatch')
globe.write_text(g.replace(old,new))
# Native full-screen desk header uses its actual category accent, without changing content/receipts.
desk=j/'Duwm1683DeskFullScreenActivity.java';d=desk.read_text()
old='TextView name=label(desk.title.toUpperCase(java.util.Locale.US),15,DuwmUnifiedTheme.TEXT,true);'
new='TextView name=label(desk.title.toUpperCase(java.util.Locale.US),15,Duwm1709SectorOutline.color(deskIndex),true);'
if d.count(old)!=1:raise RuntimeError('Build 42 full screen desk header mismatch')
desk.write_text(d.replace(old,new))
gradle=root/'app/build.gradle.kts';v=gradle.read_text();old='versionName = "1728.2.21.4.41"'
if v.count(old)!=1:raise RuntimeError('Expected Build 41 source')
gradle.write_text(v.replace(old,'versionName = "1728.2.21.4.42"'))
print('Build 42: 19 theme palette updates, 19 sector frame styles, original globe palette and native desk headers')
