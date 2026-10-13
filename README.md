# CognitiveFirewall: An Auto-Hardening Multi-Layer Defense Against LLM Prompt Injection

This is the Cognitive Firewall project powered by `Qwen` and `Qdrant`. 

## How to Run the Project

Whenever you open this project, here are the exact commands you need to spin everything up and test it:

### 1. Check your `.env` File
Before starting, ensure `FORCE_REBUILD=False` in your `.env` file unless you explicitly want it to re-download the datasets from Hugging Face and rebuild the Qdrant vectors. Setting it to `False` will make the server start up instantly.

### 2. Start the Server
Run the following Docker command to start both the Qdrant database and the Firewall application in the background:
```bash
docker compose up -d
```

### 3. Check the Logs (Optional but recommended)
To see when the Qwen model finishes loading into memory and the server is ready, stream the firewall logs:
```bash
docker logs -f firewall-app
```
*(Press `Ctrl+C` to exit the logs view at any time)*

### 4. Open the Analytics Dashboard
Open your browser and navigate to:
```
http://localhost:8000/
```
From here you can type prompts into the UI to test the firewall and view live telemetry!

### 5. Manual Dataset Update
The datasets update automatically every Sunday at 3 AM. If you want to force an update manually (e.g., after adding a new dataset to `database.py`), run:
```bash
docker exec -it firewall-app python3 -m src.main --update-datasets
```

### 6. Run the CLI Mode (Interactive Terminal)
If you want to test prompts directly in the terminal instead of the web UI:
```bash
docker exec -it firewall-app python3 -m src.main --cli
```

### 7. Run Automated Tests
Run the benchmark suite to verify the security filters:
```bash
python tests/test_cases.py
```

### 8. Shutting Down
When you are completely done for the day and want to stop the containers to free up RAM/GPU resources, run:
```bash
docker compose down
```
