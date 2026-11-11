#!/usr/bin/env python3
"""Independent public-feed smoke tests. Not proof that Android integrations work."""
import json,urllib.request,urllib.error,datetime,os
from pathlib import Path
OUT=Path("provider-audit");OUT.mkdir(exist_ok=True)
tests=[
 ("aircraft_opensky","https://opensky-network.org/api/states/all",lambda x:isinstance(x.get("states"),list)),
 ("satellite_celestrak","https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=json",lambda x:isinstance(x,list) and bool(x) and "NORAD_CAT_ID" in x[0]),
 ("weather_openmeteo","https://api.open-meteo.com/v1/forecast?latitude=0.3476&longitude=32.5825&current=temperature_2m,wind_speed_10m",lambda x: "current" in x and "time" in x["current"]),
 ("earthquakes_usgs","https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",lambda x:x.get("type")=="FeatureCollection" and isinstance(x.get("features"),list)),
]
results=[]
for name,url,validate in tests:
 entry={"feed":name,"url":url,"status":"UNTESTED","timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"DUWM-Provider-Audit/1.0 (GitHub Actions; public endpoint validation)","Accept":"application/json"})
  with urllib.request.urlopen(req,timeout=20) as response:
   body=response.read(1500000)
   entry["http_status"]=response.status
   data=json.loads(body)
   entry["status"]="PASS" if validate(data) else "FAIL_SCHEMA"
 except urllib.error.HTTPError as exc:
  entry["status"]="HTTP_ERROR";entry["http_status"]=exc.code;entry["error"]=str(exc)
 except Exception as exc:
  entry["status"]="ERROR";entry["error"]=str(exc)[:300]
 results.append(entry)
# Vessel AIS often requires a licensed key: do not claim it is working without one.
results.append({"feed":"vessel_ais","status":"NOT_VERIFIED","reason":"No authenticated AIS provider credentials configured for this independent probe"})
# RSS requires a separate parser and Android integration validation.
results.append({"feed":"news","status":"NOT_VERIFIED","reason":"News feed parsing and publication timestamps require a dedicated integration test"})
(OUT/"provider-results.json").write_text(json.dumps(results,indent=2))
with (OUT/"REPORT.md").open("w") as f:
 f.write("# DUWM public-provider network smoke audit\n\n")
 f.write("These probes check public service reachability/schema only, not the Android app or on-device behaviour.\n\n")
 f.write("| Feed | Status | HTTP |\n|---|---|---|\n")
 for x in results:f.write(f"| {x['feed']} | {x['status']} | {x.get('http_status','—')} |\n")
 f.write("\nA failed public API probe can reflect rate limiting, network access or provider outage.\n")
print((OUT/"REPORT.md").read_text())
