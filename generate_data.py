import json
import random
import urllib.parse

def clean_prop(val, default="-"):
    return val if val else default

with open('penyebaran_sekolah_tk.geojson', encoding='utf-8') as f:
    data = json.load(f)

schools = []
kindergartens = []

zones = ["North", "South", "East", "West", "Central", "North-East"]
school_types = ["Government", "Government-Aided", "Independent", "Specialised Independent"]
levels = ["Primary", "Secondary", "Secondary / JC", "Primary / Secondary", "JC"]
age_ranges = ["18 months–6 years", "2–6 years", "3–6 years", "4–6 years"]
kg_patterns = [
    ("PAP Community Foundation", "Anchor Operator"),
    ("NTUC First Campus", "Anchor Operator"),
    ("Ministry of Education", "MOE Kindergarten"),
    ("MindChamps PreSchool Pte Ltd", "Private"),
    ("EtonHouse International Education Group", "Private"),
    ("Private Operator", "Private")
]

for feature in data.get('features', []):
    props = feature.get('properties', {})
    geom = feature.get('geometry')
    amenity = props.get('amenity')
    name = props.get('name') or props.get('name:en') or "Unknown"
    
    # Address parsing from OSM tags
    address_parts = filter(None, [props.get('addr:housenumber'), props.get('addr:street')])
    address = " ".join(address_parts)
    if not address:
        address = "Singapore"
        
    postal = props.get('addr:postcode', str(random.randint(100000, 999999)))
    
    if amenity == 'school':
        search_query = urllib.parse.quote(f"{name} Singapore")
        website = props.get('website') or props.get('contact:website') or f"https://www.google.com/search?q={search_query}"
        
        schools.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {
                "name": name,
                "type": random.choice(school_types),
                "level": props.get('education') or props.get('level') or random.choice(levels),
                "address": address,
                "postal": postal,
                "zone": random.choice(zones),
                "established": random.randint(1900, 2015),
                "students": random.randint(800, 2500),
                "website": website
            }
        })
    elif amenity == 'kindergarten':
        op, typ = random.choice(kg_patterns)
        real_op = props.get('operator') or op
        
        kindergartens.append({
            "type": "Feature",
            "geometry": geom,
            "properties": {
                "name": name,
                "type": typ,
                "operator": real_op,
                "address": address,
                "postal": postal,
                "zone": random.choice(zones),
                "capacity": random.randint(50, 300),
                "age_range": random.choice(age_ranges),
                "accredited": random.random() < 0.85
            }
        })

with open("data/schools.geojson", "w", encoding='utf-8') as f:
    json.dump({"type": "FeatureCollection", "features": schools}, f, indent=2)

with open("data/kindergartens.geojson", "w", encoding='utf-8') as f:
    json.dump({"type": "FeatureCollection", "features": kindergartens}, f, indent=2)

print(f"Processed {len(schools)} schools and {len(kindergartens)} kindergartens from original GeoJSON.")
