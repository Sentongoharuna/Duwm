from pathlib import Path
import sys
root=Path(sys.argv[1])
test=root/'app/src/test/java/com/sentongoharuna/worldsituationroom/SourcePulseContractTest.java'
if not test.exists():raise RuntimeError('Build 43 test not found')
test.write_text('''package com.sentongoharuna.worldsituationroom;
import org.junit.Test;
import static org.junit.Assert.*;
import java.nio.file.*;
public class SourcePulseContractTest {
 @Test public void providerPulseMustUseRealSnapshots() throws Exception {
  Path source=Paths.get("src/main/java/com/sentongoharuna/worldsituationroom/RunningballV20LiveFeedPulse.java");
  String text=new String(Files.readAllBytes(source));
  assertTrue(text.contains("validTimestamp(v.stamp,now)"));
  assertTrue(text.contains("PROVIDER[i]+\\\"  /  \\\"+v.note"));
  assertTrue(text.contains("INVALID SOURCE TIME"));
  assertTrue(text.contains("recordChange(i,v)"));
 }
}
''')
gradle=root/'app/build.gradle.kts';s=gradle.read_text()
if 'testImplementation("junit:junit:4.13.2")' not in s:
 if 'dependencies {' not in s:raise RuntimeError('No Gradle dependencies block')
 s=s.replace('dependencies {','dependencies {\n    testImplementation("junit:junit:4.13.2")',1)
gradle.write_text(s)
print('Build 43 FIX1: corrected Java string escaping and added JUnit 4 test dependency')
