from pathlib import Path
import sys
root=Path(sys.argv[1]);j=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=j/'OperationsGlobeView.java';s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Phase 1 globe mismatch: '+a[:90])
 s=s.replace(a,b)
once('canvas.drawText("OBSERVED MARKERS "+objects.size(),dp(13),dp(19),p);',
'''// Keep diagnostic text outside the original globe's circular projection.
        float leftSafeWidth=Math.max(0f,cx-radius-dp(24));
        boolean diagnosticsFit=leftSafeWidth>p.measureText("OBSERVED MARKERS "+objects.size())+dp(13);
        if(diagnosticsFit)canvas.drawText("OBSERVED MARKERS "+objects.size(),dp(13),dp(19),p);''')
once('if(showFreshness){\n            p.setTextSize(dp(9));',
     'if(showFreshness && diagnosticsFit){\n            p.setTextSize(dp(9));')
once('canvas.drawText(moving?"EARTH ROTATION • ACTIVE":"EARTH ROTATION • PAUSED",dp(13),h-dp(18),p);',
'''if(leftSafeWidth>p.measureText("EARTH ROTATION • ACTIVE")+dp(13))
            canvas.drawText(moving?"EARTH ROTATION • ACTIVE":"EARTH ROTATION • PAUSED",dp(13),h-dp(18),p);''')
once('canvas.drawText("RENDER FRAMES "+frameCounter+"  •  ROTATION "+String.format(java.util.Locale.US,"%.1f°",totalDegrees),dp(13),h-dp(5),p);',
'''String frameDiagnostic="RENDER FRAMES "+frameCounter+"  •  ROTATION "+String.format(java.util.Locale.US,"%.1f°",totalDegrees);
        if(leftSafeWidth>p.measureText(frameDiagnostic)+dp(13))
            canvas.drawText(frameDiagnostic,dp(13),h-dp(5),p);''')
once('lastGestureEnd=SystemClock.uptimeMillis();rotationBlend=0f;focusPending=false;\n            previousFrame=lastGestureEnd;return true;',
     'lastGestureEnd=SystemClock.uptimeMillis();rotationBlend=0f;focusPending=false;\n            previousFrame=lastGestureEnd;invalidate();return true;')
p.write_text(s)
g=root/'app/build.gradle.kts';v=g.read_text();old='versionName = "1728.2.21.4.44"'
if v.count(old)!=1:raise RuntimeError('Expected Build 44 version')
g.write_text(v.replace(old,'versionName = "1728.2.21.4.45"'))
print('Build 45 Phase 1: avoid globe diagnostics overlap, keep original globe and touch animation')
