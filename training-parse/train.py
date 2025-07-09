import os
import glob
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
)

from peft import LoraConfig, get_peft_model

def prepare_dataset(md_folder: str, tokenizer, block_size: int = 1024):

    files = glob.glob(os.path.join(md_folder, "**", "*.md"), recursive=True)
    dataset = load_dataset("text", data_files={"train": files})["train"]

    def tokenize_and_chunk(examples):
        tokens = tokenizer(examples["text"], return_special_tokens_mask=False)
        input_ids = tokens["input_ids"]
        all_ids = []
        for ids in input_ids:
            all_ids.extend(ids)
        
        chunks = [all_ids[i : i + block_size] for i in range(0, len(all_ids), block_size)]
        return {"input_ids": chunks, "attention_mask": [[1] * len(c) for c in chunks]}

    tokenized = dataset.map(tokenize_and_chunk, batched=True, remove_columns=["text"])
    return tokenized

if __name__ == "__main__":
    MD_FOLDER = "../prepare-env/out"
    OUTPUT_DIR = "../.retoken"
    MODEL_ID = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
    DEVICE = "cuda"

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        load_in_8bit=True,
        device_map="auto",
    )

    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)

    train_dataset = prepare_dataset(MD_FOLDER, tokenizer, block_size=512)

    training_args = TrainingArguments(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=100,
        save_steps=500,
        output_dir=OUTPUT_DIR,
        save_total_limit=3,
    )

    trainer = Trainer(
        model=model,
        train_dataset=train_dataset,
        args=training_args,
        data_collator=lambda data: {
            "input_ids": tokenizer.pad(
                {"input_ids": [f["input_ids"] for f in data]},
                return_tensors="pt",
            )["input_ids"],
            "attention_mask": tokenizer.pad(
                {"input_ids": [f["input_ids"] for f in data]},
                return_tensors="pt",
            )["attention_mask"],
            "labels": tokenizer.pad(
                {"input_ids": [f["input_ids"] for f in data]},
                return_tensors="pt",
            )["input_ids"],
        },
    )

    trainer.train()
    trainer.save_model(OUTPUT_DIR)
