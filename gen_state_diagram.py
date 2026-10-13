import base64
import zlib
import urllib.request

puml = """@startuml
skinparam monochrome false
skinparam handwritten false

state "Idle / Traffic Monitoring" as Monitor
state "Zero-Day Detected (Layer 2)" as Detect
state "Malicious Intent Extraction" as Extract
state "Vector Embedding (SBERT)" as Embed
state "Qdrant Database Upsert" as Upsert
state "Hardened State Active" as Hardened

[*] --> Monitor
Monitor --> Detect : Novel Attack Bypasses L1
Detect --> Extract : Parse Qwen XML Output
Extract --> Embed : Encode Raw Threat Text
Embed --> Upsert : HTTP PUT to Vector DB
Upsert --> Hardened : Layer 1 Rules Updated
Hardened --> Monitor : Resume Defense
@enduml"""

compressed = zlib.compress(puml.encode('utf-8'), 9)
encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
url = f"https://kroki.io/plantuml/png/{encoded}"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    with open(r'c:\Users\moham\OneDrive\Documents\my-qdrant-project\screenshots\auto_hardening_state.png', 'wb') as out_file:
        out_file.write(response.read())

print("Downloaded auto_hardening_state.png successfully!")
