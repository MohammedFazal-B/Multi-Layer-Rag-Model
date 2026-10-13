import os
import sys
from src.database import setup_database_and_embed
from src.llm import setup_llm
from src.server import run_server
from src.firewall_core import check_user_input
from src.config import SIMILARITY_THRESHOLD

def print_check_result(prompt, result):
    print(f"\\nUser Input: '{prompt}'")
    if result["status"] == "BLOCK":
        matched = (result.get("matched_against") or "")[:100]
        print(f"ACTION: {result['status']} (Score: {result['score']})")
        if matched:
            print(f"   Matched threat: '{matched}...'")
    else:
        print(f"ACTION: {result['status']} (Score: {result.get('score', 0)})")
        if result.get("reason"):
            print(f"   {result['reason']}")


def run_cli(model, client, llm):
    print("\n" + "=" * 50)
    print("RAG prompt firewall (interactive)")
    print("=" * 50)
    print(f"Threshold: {SIMILARITY_THRESHOLD}")
    print("Type a prompt and press Enter. Empty line, quit, or exit to stop.\n")
    
    history = []
    
    while True:
        try:
            prompt = input("Prompt> ")
        except (EOFError, KeyboardInterrupt):
            print("\nStopping.")
            break
        if prompt.strip().lower() in {"", "quit", "exit"}:
            break
            
        result = check_user_input(prompt, model, client, llm, history=history)
        print_check_result(prompt, result)
        
        if result["status"] == "ALLOW":
            history.append({"role": "user", "content": prompt})
            history.append({"role": "assistant", "content": "Simulated response."})
            print(f"(Context updated: {len(history)//2} turns in memory)")


from apscheduler.schedulers.background import BackgroundScheduler
from src.database import setup_database_and_embed, update_datasets_job

def main():
    model, client = setup_database_and_embed()
    
    if "--update-datasets" in sys.argv:
        print("\n--- Manual Dataset Update Triggered ---")
        update_datasets_job(client)
        print("--- Update Complete ---")
        sys.exit(0)
        
    llm = setup_llm()
    mode = "cli" if "--cli" in sys.argv else os.getenv("FIREWALL_MODE", "server")
    
    # Start background job for dataset updates
    scheduler = BackgroundScheduler()
    # Runs weekly on Sunday at 3 AM
    scheduler.add_job(update_datasets_job, 'cron', args=[client], day_of_week='sun', hour=3)
    scheduler.start()
    print("Background dataset updater scheduled (weekly on Sunday at 3 AM).")
    
    try:
        if mode == "cli":
            run_cli(model, client, llm)
        else:
            run_server(model, client, llm)
    finally:
        client.close()

if __name__ == "__main__":
    main()
