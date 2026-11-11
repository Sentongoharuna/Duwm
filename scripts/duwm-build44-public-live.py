from pathlib import Path
import sys
root=Path(sys.argv[1]);java=root/'app/src/main/java/com/sentongoharuna/worldsituationroom'
p=java/'RunningballV25GlobalAircraftData.java';s=p.read_text()
def once(a,b):
 global s
 if s.count(a)!=1:raise RuntimeError('Build 44 anchor mismatch: '+a[:95])
 s=s.replace(a,b)
once('public boolean hasGood(){return receivedAt>0&&providerRows>=0&&positionRows>=0;}',
'''public boolean hasGood(){return receivedAt>0&&receivedAt<=System.currentTimeMillis()+120000L
      &&providerRows>=0&&positionRows>=0&&sourceAt>0&&sourceAt<=System.currentTimeMillis()+120000L;}''')
once('if(!hasGood())return error.isEmpty()?"NO VERIFIED GLOBAL AIRCRAFT DATA": (lastHttp==429?"RATE LIMITED / NO DATA":"SOURCE FAILED / NO DATA");',
'''if(!hasGood())return error.isEmpty()?"NO VERIFIED GLOBAL AIRCRAFT DATA":
        (lastHttp==429?"RATE LIMITED / NO DATA":lastHttp==401?"AUTHENTICATION REQUIRED / PUBLIC DATA UNAVAILABLE":"SOURCE FAILED / NO DATA");''')
once('if(sourceAt>0&&System.currentTimeMillis()-sourceAt>CACHE_TTL_MS)return "STALE / PROVIDER TIME";',
'''if(sourceAt>0&&System.currentTimeMillis()-sourceAt>CACHE_TTL_MS)return "STALE / PROVIDER TIME";''')
once('if(sourceAt<=0)return "PROVIDER TIMESTAMP MISSING";',
     'if(sourceAt<=0||sourceAt>System.currentTimeMillis()+120000L)return "PROVIDER TIMESTAMP INVALID";')
once('String retry=connection.getHeaderField("X-Rate-Limit-Retry-After-Seconds");',
'''String retry=connection.getHeaderField("X-Rate-Limit-Retry-After-Seconds");
        if(retry==null||retry.trim().isEmpty())retry=connection.getHeaderField("Retry-After");''')
once('if(http==429){\n          try{pause=Math.max(pause,Math.min(604800L,Long.parseLong(retry))*1000L);}catch(Exception ignored){}\n        }',
'''if(http==429){
          try{pause=Math.max(pause,Math.min(604800L,Long.parseLong(retry.trim()))*1000L);}catch(Exception ignored){}
        }''')
p.write_text(s)
g=root/'app/build.gradle.kts';t=g.read_text();old='versionName = "1728.2.21.4.43.2"'
if t.count(old)!=1:raise RuntimeError('Build 43.2 version missing')
g.write_text(t.replace(old,'versionName = "1728.2.21.4.44"'))
print('Build 44: OpenSky anonymous requests retained; invalid future timestamps, 401 and 429/Retry-After handled clearly')
