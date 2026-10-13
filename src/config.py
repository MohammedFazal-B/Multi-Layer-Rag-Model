import os

# --- Configuration ---
COLLECTION_NAME = "prompt_firewall"
EMBEDDING_MODEL_NAME = "BAAI/bge-large-en-v1.5"
SIMILARITY_THRESHOLD = 0.85
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
FORCE_REBUILD = os.getenv("FORCE_REBUILD", "false").lower() in {"1", "true", "yes"}
FIREWALL_HOST = os.getenv("FIREWALL_HOST", "0.0.0.0")
FIREWALL_PORT = int(os.getenv("FIREWALL_PORT", "8000")) 

HF_DATASETS = {
    "xTRam1/safe-guard-prompt-injection": None,
    "neuralchemy/Prompt-injection-dataset": None,
    "deepset/prompt-injections": None,
    "JailbreakBench/JBB-Behaviors": "behaviors", 
    "lmsys/toxic-chat": "toxicchat1123", 
    "PKU-Alignment/BeaverTails": None,
    "allenai/wildguardmix": "wildguardtrain" 
}
