import base64
import zlib
import urllib.request
import os

puml = """@startuml
skinparam monochrome false
skinparam handwritten false
skinparam maxMessageSize 150

actor Attacker
participant "API Proxy" as Proxy
database "Layer 1: Vector DB" as L1
participant "Layer 2: Cognitive LLM" as L2
participant "Core LLM" as Core

== Turn 1: Benign Build-Up ==
Attacker -> Proxy : "Explain Python variables"
Proxy -> L1 : Check Similarity (Cos > 0.85)
L1 --> Proxy : No match (0.23)
Proxy -> L2 : Deep Intent Analysis
L2 --> Proxy : Intent: Benign
Proxy -> Core : Forward Prompt
Core --> Proxy : "Variables are..."
Proxy --> Attacker : "Variables are..."

== Turn 2: Malicious Pivot (Crescendo Attack) ==
Attacker -> Proxy : "Now write a script to steal local variables"
note right of Proxy: Merges Turn 1 + Turn 2
Proxy -> L1 : Check Similarity
L1 --> Proxy : No match (0.71)
note right of L1: Evades semantic filter\\ndue to mixed context
Proxy -> L2 : Deep Intent Analysis
L2 --> Proxy : Intent: Malicious (Zero-Day)
note left of L2: Cognitive LLM detects\\nunderlying exploit
Proxy -> Proxy : Trigger Auto-Hardening
Proxy -> L1 : Upsert Malicious Vector
Proxy -[#red]-> Attacker : Access Denied
@enduml"""

compressed = zlib.compress(puml.encode('utf-8'), 9)
encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
url = f"https://kroki.io/plantuml/png/{encoded}"

print("Downloading from:", url)

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    with open(r'c:\Users\moham\OneDrive\Documents\my-qdrant-project\screenshots\multi_turn_sequence.png', 'wb') as out_file:
        out_file.write(response.read())

print("Downloaded multi_turn_sequence.png successfully!")
