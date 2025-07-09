import os
import subprocess
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL_ID = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
LORA_ADAPTER_PATH = "../.retoken"
MERGED_OUTPUT_DIR = "../.tokenmapping"
CONVERT_SCRIPT = "../llama.cpp/convert_hf_to_gguf.py"
GGUF_OUTPUT = "../osg-ai/osg-ai.gguf"

print("Loading base model and tokenizer...")
base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_ID)
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)

print("Loading LoRA adapter and merging with base model...")
peft_model = PeftModel.from_pretrained(base_model, LORA_ADAPTER_PATH)
merged_model = peft_model.merge_and_unload()

print(f"Saving merged model to {MERGED_OUTPUT_DIR} ...")
os.makedirs(MERGED_OUTPUT_DIR, exist_ok=True)
merged_model.save_pretrained(MERGED_OUTPUT_DIR)
tokenizer.save_pretrained(MERGED_OUTPUT_DIR)

print("Converting merged model to GGUF format (q8_0 quantization)...")
convert_cmd = [
    sys.executable,
    CONVERT_SCRIPT,
    MERGED_OUTPUT_DIR,
    "--outfile", GGUF_OUTPUT,
    "--outtype", "q8_0"
]

subprocess.run(convert_cmd, check=True)
print(f"GGUF model saved as {GGUF_OUTPUT}.")
