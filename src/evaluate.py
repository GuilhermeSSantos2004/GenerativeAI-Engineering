"""Avaliação GPU: mesmas perguntas de teste para modelo base e fine-tuned."""
import argparse
import json
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.common import MODEL_ID, generate_answer, normalize, read_jsonl, require_gpu


def evaluate_prediction(text, expected_keywords):
    plain = normalize(text)
    hits = [term for term in expected_keywords if normalize(term) in plain]
    structural = (
        "causa:" in plain
        and "correcao:" in plain
        and "codigo corrigido:" in plain
    )
    recall = len(hits) / max(1, len(expected_keywords))
    return {
        "format_ok": structural,
        "keyword_recall": round(recall, 4),
        "all_keywords": len(hits) == len(expected_keywords),
        "keyword_hits": hits,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--test-file", default="data/test.jsonl")
    p.add_argument("--adapter", default="", help="Caminho do final_adapter; vazio = base")
    p.add_argument("--output", required=True)
    p.add_argument("--max-new-tokens", type=int, default=180)
    p.add_argument("--temperature", type=float, default=0, help="0 = greedy e reproduzível")
    args = p.parse_args()
    device = require_gpu()
    if args.temperature < 0:
        raise ValueError("--temperature deve ser >= 0")
    cases = read_jsonl(args.test_file)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=torch.float16
    ).to("cuda")
    if args.adapter:
        adapter_path = Path(args.adapter)
        if not adapter_path.exists():
            raise FileNotFoundError(f"Adapter não encontrado: {adapter_path}")
        model = PeftModel.from_pretrained(model, str(adapter_path), is_trainable=False)
    model.eval()
    rows = []
    per_category = defaultdict(list)
    for case in cases:
        start = time.perf_counter()
        answer = generate_answer(
            model,
            tokenizer,
            case["prompt"],
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
        )
        elapsed = time.perf_counter() - start
        grading = evaluate_prediction(answer, case["expected_keywords"])
        rows.append({
            "id": case["id"],
            "category": case["category"],
            "prompt": case["prompt"],
            "expected_answer": case["answer"],
            "expected_keywords": case["expected_keywords"],
            "generated_answer": answer,
            "latency_seconds": round(elapsed, 3),
            **grading,
        })
        per_category[case["category"]].append(grading["keyword_recall"])
        print(f"{case['id']}: formato={grading['format_ok']}, "
              f"recall={grading['keyword_recall']:.2f}, tempo={elapsed:.2f}s")
    n = len(rows)
    report = {
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "model": MODEL_ID,
        "variant": "fine_tuned" if args.adapter else "baseline",
        "adapter": args.adapter or None,
        "gpu": device,
        "temperature": args.temperature,
        "sample_count": n,
        "format_rate": round(sum(x["format_ok"] for x in rows) / n, 4),
        "keyword_recall": round(sum(x["keyword_recall"] for x in rows) / n, 4),
        "full_keyword_rate": round(sum(x["all_keywords"] for x in rows) / n, 4),
        "mean_latency_seconds": round(sum(x["latency_seconds"] for x in rows) / n, 3),
        "category_keyword_recall": {
            key: round(sum(vals) / len(vals), 4)
            for key, vals in sorted(per_category.items())
        },
        "methodology": (
            "Métricas automáticas auxiliares: taxa de formato e presença "
            "de palavras-chave; não medem correção semântica completa. "
            "Avaliadores devem inspecionar as respostas geradas."
        ),
        "examples": rows,
    }
    dest = Path(args.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "examples"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
