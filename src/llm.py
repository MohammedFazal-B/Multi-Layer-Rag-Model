from llama_cpp import Llama

def setup_llm():
    print("\nInitializing Qwen Cognitive Defense Layer...")
    try:
        llm = Llama(
            model_path="models/Qwen3.5-9B.Q4_K_M.gguf",
            n_ctx=2048,
            n_gpu_layers=24, # Leave some layers on CPU to free up VRAM
            verbose=False
        )
        print("Qwen model loaded successfully.")
        return llm
    except Exception as e:
        print(f"Failed to load Qwen model: {e}")
        print("Cognitive Defense Layer will be disabled.")
        return None
