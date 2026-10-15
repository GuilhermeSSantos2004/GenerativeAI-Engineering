"""Fine-tuning LoRA reproduzível: execute somente com GPU CUDA ativa."""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import torch
from peft import LoraConfig, TaskType, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    set_seed,
)

from src.common import MODEL_ID, Collator, SupervisedExamples, read_jsonl, require_gpu


def args_cli():
    p = argparse.ArgumentParser(description="Fine-tuning LoRA da Qwen2.5-0.5B-Instruct")
    p.add_argument("--train-file", default="data/train.jsonl")
    p.add_argument("--val-file", default="data/val.jsonl")
    p.add_argument("--output-dir", required=True)
    p.add_argument("--learning-rate", type=float, default=2e-4)
    p.add_argument("--epochs", type=float, default=2.0)
    p.add_argument("--batch-size", type=int, default=2)
    p.add_argument("--grad-accum", type=int, default=4)
    p.add_argument("--lora-r", type=int, default=8)
    p.add_argument("--max-length", type=int, default=384)
    p.add_argument("--max-steps", type=int, default=-1)
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()


def main():
    args = args_cli()
    gpu_name = require_gpu()
    if args.learning_rate <= 0 or args.lora_r <= 0 or args.epochs <= 0:
        raise ValueError("Hiperparâmetros devem ser positivos")
    set_seed(args.seed)
    torch.cuda.reset_peak_memory_stats()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    records_train = read_jsonl(args.train_file)
    records_val = read_jsonl(args.val_file)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    data_train = SupervisedExamples(records_train, tokenizer, args.max_length)
    data_val = SupervisedExamples(records_val, tokenizer, args.max_length)
    base = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
    base.config.use_cache = False
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=args.lora_r,
        lora_alpha=args.lora_r * 2,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"],
        bias="none",
    )
    model = get_peft_model(base, lora_config)
    model.print_trainable_parameters()
    config = TrainingArguments(
        output_dir=str(out / "checkpoints"),
        learning_rate=args.learning_rate,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        max_steps=args.max_steps,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        optim="adamw_torch",
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="steps",
        logging_steps=5,
        save_total_limit=1,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        report_to="none",
        seed=args.seed,
        data_seed=args.seed,
        remove_unused_columns=False,
        dataloader_num_workers=0,
    )
    trainer = Trainer(
        model=model,
        args=config,
        train_dataset=data_train,
        eval_dataset=data_val,
        data_collator=Collator(tokenizer),
        processing_class=tokenizer,
    )
    start = time.time()
    train_result = trainer.train()
    validation = trainer.evaluate()
    adapter_path = out / "final_adapter"
    trainer.save_model(str(adapter_path))
    tokenizer.save_pretrained(str(adapter_path))
    summary = {
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "base_model": MODEL_ID,
        "adapter_path": str(adapter_path),
        "gpu": gpu_name,
        "cuda_version": torch.version.cuda,
        "torch_version": torch.__version__,
        "train_examples": len(records_train),
        "val_examples": len(records_val),
        "config": vars(args),
        "train_metrics": train_result.metrics,
        "val_metrics": validation,
        "elapsed_seconds": round(time.time() - start, 2),
        "max_gpu_memory_gb": round(torch.cuda.max_memory_allocated() / 1024 ** 3, 3),
    }
    (out / "metrics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
    (out / "history.json").write_text(
        json.dumps(trainer.state.log_history, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    print("Adapter LoRA salvo em:", adapter_path.resolve())


if __name__ == "__main__":
    main()
