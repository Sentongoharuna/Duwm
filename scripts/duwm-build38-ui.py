from pathlib import Path
import sys
root=Path(sys.argv[1])
java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
theme=java/'DuwmUnifiedTheme.java'
s=theme.read_text()
def once(old,new):
 global s
 if s.count(old)!=1: raise RuntimeError('Build 38 theme mismatch: '+old)
 s=s.replace(old,new)
# Apply a cohesive dark-navy hierarchy to the existing app-wide theme constants,
# rather than only declaring unused colour values.
once('public static final int PANEL = 0xFF041424;', 'public static final int PANEL = 0xFF0B2035;')
once('public static final int PANEL_SELECTED = 0xFF061626;', 'public static final int PANEL_SELECTED = 0xFF12304B;')
once('public static final int BORDER = 0xFFDEE5EF;', 'public static final int BORDER = 0xFF37617D;')
once('public static final int DIVIDER = 0xFF7D8E9F;', 'public static final int DIVIDER = 0xFF24435E;')
once('public static final int SECTOR_LINE = 0xFFBDC7D2;', 'public static final int SECTOR_LINE = 0xFF427390;')
once('public static final int FORMAL_CORNER_DP = 20;', 'public static final int FORMAL_CORNER_DP = 14;')
once('public static final int RAISED_CARD = PANEL;', 'public static final int RAISED_CARD = 0xFF102C46;')
once('public static final int MUTED = 0xFFA0A5AE;', 'public static final int MUTED = 0xFFB0C4D6;')
once('public static final int MAP_COAST = 0xFF28547A;', 'public static final int MAP_COAST = 0xFF38789B;')
once('public static final int MAP_BORDER = 0xFF173B5B;', 'public static final int MAP_BORDER = 0xFF255579;')
once('public static final int MAP_RIM = 0xFF184472;', 'public static final int MAP_RIM = 0xFF2870A0;')
once('public static final int MAP_GRID = 0xFF0D2439;', 'public static final int MAP_GRID = 0xFF18364D;')
theme.write_text(s)
gradle=root/'app/build.gradle.kts'
g=gradle.read_text()
old='versionName = "1728.2.21.4.37.1"'
if g.count(old)!=1: raise RuntimeError('Build 37.1 base missing')
gradle.write_text(g.replace(old,'versionName = "1728.2.21.4.38"'))
print('Build 38: 12 shared visual theme values changed across screens that use DuwmUnifiedTheme')
