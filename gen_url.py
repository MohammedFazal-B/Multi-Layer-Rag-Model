import base64
import zlib

graph = """graph TD
    User(User Application) -->|Prompt + History| API[API Gateway / Proxy]
    
    subgraph Layer1 [Layer 1: Semantic Vector Shield]
        API --> Chunk[Sliding Window Chunking]
        Chunk --> Embed[Sentence Transformer Embeddings]
        Embed --> Qdrant[(Qdrant Vector Database)]
        Qdrant --> Math{Cosine > 0.85?}
    end
    
    Math -- Yes: Known Attack --> Blocked(Access Denied / Blocked)
    Math -- No: Novel Prompt --> Context
    
    subgraph Layer2 [Layer 2: Cognitive Evaluator]
        Context[XML Context Formatting]
        Context --> Qwen[Local Qwen LLM Inference]
        Qwen --> Intent{Intent Malicious?}
    end
    
    Intent -- Yes: Zero-Day --> AutoHarden[Dynamic Auto-Hardening]
    AutoHarden -. Upsert Payload .-> Qdrant
    AutoHarden --> Blocked
    
    Intent -- No: Benign --> Allowed(Access Granted)
    Allowed --> CoreAI[[Production LLM Core]]"""

encoded = base64.urlsafe_b64encode(zlib.compress(graph.encode('utf-8'), 9)).decode('ascii')
url = f"https://mermaid.ink/img/pako:{encoded}?type=png"
print(url)
