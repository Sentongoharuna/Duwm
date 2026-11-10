from pathlib import Path
import sys
root=Path(sys.argv[1]); p=root/'app/src/main/java/com/sentongoharuna/worldsituationroom/Duwm1718MonitorsCamActivity.java'
s=p.read_text()
def change(a,b):
 global s
 if s.count(a)!=1: raise RuntimeError(f'expected once, got {s.count(a)}: {a[:70]}')
 s=s.replace(a,b)
