#!/usr/bin/env python3
"""Provider-specific checks. A network probe is not an Android integration test."""
import os,json,urllib.request,urllib.error,datetime,xml.etree.ElementTree as ET
from pathlib import Path
out=Path("provider-audit");out.mkdir(exist_ok=True)
now=datetime.datetime.now(datetime.timezone.utc)
results=[]
feeds=[
 ("news_bbc_world","https://feeds.bbci.co.uk/news/world/rss.xml"),
 ("news_aljazeera","https://www.aljazeera.com/xml/rss/all.xml"),
 ("news_guardian_world","https://www.theguardian.com/world/rss"),
]
for name,url in feeds:
 item={"feed":name,"status":"UNTESTED","url":url}
 try:
  request=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; DUWM-SourceAudit/1.0)","Accept":"application/rss+xml, application/atom+xml, application/xml, text/xml"})
  with urllib.request.urlopen(request,timeout=25) as response:
   raw=response.read(1800000);item["http_status"]=response.status
  root=ET.fromstring(raw)
  entries=root.findall(".//item")
  if not entries:entries=root.findall(".//{http://www.w3.org/2005/Atom}entry")
  valid=0;missing_date=0;missing_link=0
  for entry in entries[:30]:
   title=(entry.findtext("title") or entry.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
   date=(entry.findtext("pubDate") or entry.findtext("{http://www.w3.org/2005/Atom}updated") or entry.findtext("{http://www.w3.org/2005/Atom}published") or "").strip()
   link=(entry.findtext("link") or "").strip()
   if not link:
    el=entry.find("{http://www.w3.org/2005/Atom}link")
    if el is not None:link=el.attrib.get("href","")
   if not date:missing_date+=1
   if not link:missing_link+=1
   if title and date and link:valid+=1
  item.update({"entries_seen":len(entries),"valid_title_date_link":valid,"missing_date":missing_date,"missing_link":missing_link})
  item["status"]="PASS" if valid>0 else "FAIL_SCHEMA"
 except urllib.error.HTTPError as exc:item.update({"status":"HTTP_ERROR","http_status":exc.code,"error":str(exc)})
 except Exception as exc:item.update({"status":"ERROR","error":str(exc)[:250]})
 results.append(item)
# AIS providers generally require credentials. Test only when an explicit endpoint and key are configured.
endpoint=os.getenv("DUWM_AIS_PROBE_URL","").strip()
token=os.getenv("DUWM_AIS_API_KEY","").strip()
ais={"feed":"vessel_ais","status":"NOT_CONFIGURED","reason":"Requires an authorized AIS provider URL and token; never synthesize vessel positions"}
if endpoint and token and endpoint.startswith("https://"):
 try:
  req=urllib.request.Request(endpoint,headers={"Authorization":"Bearer "+token,"Accept":"application/json","User-Agent":"DUWM-SourceAudit/1.0"})
  with urllib.request.urlopen(req,timeout=25) as response:
   data=json.loads(response.read(1500000));ais["http_status"]=response.status
  ais["status"]="PASS_RESPONSE" if isinstance(data,(list,dict)) else "FAIL_SCHEMA"
  ais["reason"]="Authenticated response received; vessel positions and licensing not yet validated"
 except urllib.error.HTTPError as exc:ais.update({"status":"HTTP_ERROR","http_status":exc.code,"reason":"Authenticated request rejected"})
 except Exception as exc:ais.update({"status":"ERROR","reason":type(exc).__name__})
elif endpoint or token:ais["reason"]="Both HTTPS AIS endpoint and API token must be configured"
results.append(ais)
(out/"news-ais-results.json").write_text(json.dumps(results,indent=2))
with (out/"NEWS-AIS-REPORT.md").open("w") as f:
 f.write("# DUWM News and AIS verification\n\n")
 f.write("Network/schema tests only. They do not verify the APK's actual news cards or vessel tracking.\n\n")
 f.write("| Source | Status | HTTP | Complete entries |\n|---|---|---|---|\n")
 for x in results:f.write(f"| {x['feed']} | {x['status']} | {x.get('http_status','—')} | {x.get('valid_title_date_link','—')} |\n")
 f.write("\nMissing or rejected AIS credentials are reported honestly; no fabricated vessel positions.\n")
print((out/"NEWS-AIS-REPORT.md").read_text())
