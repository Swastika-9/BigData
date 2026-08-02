from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd

NS={"tx":"http://www.transxchange.org.uk/"}
RAW_DIR=Path("data/raw")
OUT_DIR=Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

stops=[];operators=[];services=[];routes=[];route_links=[];jp_links=[];vehicle_journeys=[]

def t(e,p):
    x=e.find(p,NS)
    return x.text.strip() if x is not None and x.text else None

for xml in RAW_DIR.glob("*.xml"):
    root=ET.parse(xml).getroot()
    for s in root.findall(".//tx:AnnotatedStopPointRef",NS):
        stops.append({
            "stop_point_ref":t(s,"tx:StopPointRef"),
            "common_name":t(s,"tx:CommonName"),
            "indicator":t(s,"tx:Indicator"),
            "locality_name":t(s,"tx:LocalityName"),
            "locality_qualifier":t(s,"tx:LocalityQualifier")
        })
    for o in root.findall(".//tx:Operator",NS):
        operators.append({
            "operator_id":o.get("id"),
            "operator_code":t(o,"tx:OperatorCode"),
            "operator_short_name":t(o,"tx:OperatorShortName"),
            "operator_name":t(o,"tx:OperatorName")
        })
    for s in root.findall(".//tx:Service",NS):
        services.append({
            "service_code":t(s,"tx:ServiceCode"),
            "line_name":t(s,"tx:Lines/tx:Line/tx:LineName"),
            "origin":t(s,"tx:StandardService/tx:Origin"),
            "destination":t(s,"tx:StandardService/tx:Destination")
        })
    for r in root.findall(".//tx:Route",NS):
        routes.append({"route_id":r.get("id"),"description":t(r,"tx:Description")})
    for rl in root.findall(".//tx:RouteLink",NS):
        route_links.append({
            "route_link_id":rl.get("id"),
            "from_stop":t(rl,"tx:From/tx:StopPointRef"),
            "to_stop":t(rl,"tx:To/tx:StopPointRef"),
            "distance":t(rl,"tx:Distance")
        })
    for j in root.findall(".//tx:JourneyPatternTimingLink",NS):
        jp_links.append({
            "timing_link_id":j.get("id"),
            "from_stop":t(j,"tx:From/tx:StopPointRef"),
            "from_activity":t(j,"tx:From/tx:Activity"),
            "to_stop":t(j,"tx:To/tx:StopPointRef"),
            "to_activity":t(j,"tx:To/tx:Activity"),
            "route_link_ref":t(j,"tx:RouteLinkRef"),
            "run_time":t(j,"tx:RunTime")
        })
    for v in root.findall(".//tx:VehicleJourney",NS):
        vehicle_journeys.append({
            "vehicle_journey_code":t(v,"tx:VehicleJourneyCode"),
            "service_ref":t(v,"tx:ServiceRef"),
            "line_ref":t(v,"tx:LineRef"),
            "journey_pattern_ref":t(v,"tx:JourneyPatternRef"),
            "departure_time":t(v,"tx:DepartureTime"),
            "operator_ref":t(v,"tx:OperatorRef")
        })

tables={
"stops.csv":stops,
"operators.csv":operators,
"services.csv":services,
"routes.csv":routes,
"route_links.csv":route_links,
"journey_pattern_links.csv":jp_links,
"vehicle_journeys.csv":vehicle_journeys
}
for name,data in tables.items():
    pd.DataFrame(data).drop_duplicates().to_csv(OUT_DIR/name,index=False)

print("Done")