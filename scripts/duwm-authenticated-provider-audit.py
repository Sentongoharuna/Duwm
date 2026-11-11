#!/usr/bin/env python3
"""Authenticated OpenSky OAuth2 and AISStream WebSocket checks; no secret logging."""
import os,json,datetime,urllib.request,urllib.error,asyncio
from pathlib import Path
out=Path("provider-audit");out.mkdir(exist_ok=True)
results=[]
client=os.getenv("OPENSKY_CLIENT_ID","").strip();secret=os.getenv("OPENSKY_CLIENT_SECRET","").strip()
air={"provider":"OpenSky OAuth2","status":"NOT_CONFIGURED"}
if client and secret:
 try:
  import urllib.parse
  body=urllib.parse.urlencode({"grant_type":"client_credentials","client_id":client,"client_secret":secret}).encode()
  req=urllib.request.Request("https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token",data=body,headers={"Content-Type":"application/x-www-form-urlencoded"},method="POST")
  with urllib.request.urlopen(req,timeout=20) as response: token=json.loads(response.read(200000)).get("access_token","")
  if not token:raise ValueError("Token missing")
  req=urllib.request.Request("https://opensky-network.org/api/states/all?lamin=-1&lomin=30&lamax=2&lomax=35",headers={"Authorization":"Bearer "+token,"User-Agent":"DUWM-Audit/1.0"})
  with urllib.request.urlopen(req,timeout=25) as response:data=json.loads(response.read(1000000));air["http_status"]=response.status
  air["status"]="PASS" if isinstance(data.get("states"),list) else "FAIL_SCHEMA"
 except urllib.error.HTTPError as exc:air.update(status="HTTP_ERROR",http_status=exc.code)
 except Exception as exc:air.update(status="ERROR",error=type(exc).__name__)
elif client or secret:air["status"]="PARTIAL_CONFIGURATION"
results.append(air)
ais_key=os.getenv("DUWM_AIS_API_KEY","").strip()
ais={"provider":"AISStream WebSocket","status":"NOT_CONFIGURED"}
if ais_key:
 try:
  import websockets
  async def check():
   async with websockets.connect("wss://stream.aisstream.io/v0/stream",open_timeout=15,close_timeout=5,max_size=1000000) as ws:
    subscription={"APIKey":ais_key,"BoundingBoxes":[[[-1,29],[4,36]]],"FilterMessageTypes":["PositionReport"]}
    await ws.send(json.dumps(subscription))
    msg=await asyncio.wait_for(ws.recv(),timeout=25)
    data=json.loads(msg)
    if "error" in data or "Error" in data:return "PROVIDER_ERROR"
    if "MessageType" in data or "Message" in data:return "PASS_RESPONSE"
    return "UNRECOGNIZED_RESPONSE"
  ais["status"]=asyncio.run(check())
 except asyncio.TimeoutError:ais["status"]="TIMEOUT_NO_MESSAGES"
 except Exception as exc:ais.update(status="ERROR",error=type(exc).__name__)
results.append(ais)
(out/"authenticated-results.json").write_text(json.dumps(results,indent=2))
with (out/"AUTHENTICATED-REPORT.md").open("w") as f:
 f.write("# DUWM authenticated provider audit\n\n")
 f.write("These are independent API probes, not proof of Android playback or position rendering.\n\n")
 for r in results:f.write(f"- {r['provider']}: **{r['status']}**\n")
 f.write("\nSecrets are never written to this report. AIS requires valid account credentials and may not deliver a position during a short test window.\n")
print((out/"AUTHENTICATED-REPORT.md").read_text())
