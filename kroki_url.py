import base64
import zlib

puml = """@startuml
skinparam handwritten false
skinparam monochrome false
skinparam packageStyle rectangle

actor "User Application" as User
node "API Gateway / Proxy" as API

package "Layer 1: Semantic Vector Shield" {
    [Sliding Window Chunking] as Chunk
    [Sentence Transformer] as Embed
    database "Qdrant Vector DB" as Qdrant
    hexagon "Cosine > 0.85?" as Math
}

package "Layer 2: Cognitive Evaluator" {
    [XML Context Formatting] as Context
    [Local Qwen LLM] as Qwen
    hexagon "Intent Malicious?" as Intent
}

[Access Denied (Blocked)] as Blocked
[Dynamic Auto-Hardening] as AutoHarden
[Access Granted] as Allowed
cloud "Production LLM Core" as CoreAI

User --> API : Prompt + History
API --> Chunk
Chunk --> Embed
Embed --> Qdrant
Qdrant --> Math

Math -[#red]-> Blocked : Yes: Known Attack
Math -[#green]-> Context : No: Novel Prompt

Context --> Qwen
Qwen --> Intent

Intent -[#red]-> AutoHarden : Yes: Zero-Day
AutoHarden .> Qdrant : Upsert Payload
AutoHarden -[#red]-> Blocked

Intent -[#green]-> Allowed : No: Benign
Allowed --> CoreAI
@enduml
"""

# Kroki uses zlib (deflate) + base64 URL safe
compressed = zlib.compress(puml.encode('utf-8'), 9)
encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
url = f"https://kroki.io/plantuml/svg/{encoded}"
print(url)
