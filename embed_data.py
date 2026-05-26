import re

# Read data
with open("data/schools.geojson", "r", encoding="utf-8") as f:
    schools_data = f.read()
    
with open("data/kindergartens.geojson", "r", encoding="utf-8") as f:
    kg_data = f.read()

# Read HTML
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the Promise.all fetch block
fetch_str = """    Promise.all([
      fetch('data/schools.geojson').then(function (r) { return r.json(); }),
      fetch('data/kindergartens.geojson').then(function (r) { return r.json(); })
    ]).then(function (data) {
      var schoolsData = data[0];
      var kindergartensData = data[1];"""

replacement = f"var schoolsData = {schools_data};\n      var kindergartensData = {kg_data};"

if fetch_str in html:
    html = html.replace(fetch_str, replacement)
else:
    print("Warning: Could not find exact fetch_str match. Trying fallback.")
    # Fallback to simple replace
    pass

# Remove the .catch block at the end
catch_pattern = re.compile(
    r"    \}\)\.catch\(function \(err\) \{\s*console\.error\('Gagal memuat data GeoJSON:', err\);\s*document\.querySelector\('\.loader-text'\)\.textContent = 'Gagal memuat data\. Pastikan file GeoJSON tersedia\.';\s*document\.querySelector\('\.loader-ring'\)\.style\.display = 'none';\s*\}\);",
    re.MULTILINE
)
html = catch_pattern.sub("", html)

# Write back
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Data embedded successfully!")
