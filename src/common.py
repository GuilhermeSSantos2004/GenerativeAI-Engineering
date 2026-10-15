"""Dataset, formatação de prompts e inferência da LLM sem API proprietária."""
import json
import unicodedata
from pathlib import Path

import torch
from torch.utils.data import Dataset

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
SYSTEM_PROMPT = (
    "Você é um assistente de depuração de Python. Responda SOMENTE em português. "
    "Diagnostique o erro apresentado, não invente contexto e organize a resposta "
    "usando exatamente os títulos 'Causa:', 'Correção:' e 'Código corrigido:'. "
    "Inclua um trecho Python corrigido curto e executável quando possível."
)


def require_gpu():
    """Falhar explicitamente caso um experimento avaliado esteja sem GPU CUDA."""
    if not torch.cuda.is_available():
        raise RuntimeError(
            "GPU CUDA não disponível. No Colab, selecione Ambiente de execução > "
            "Alterar tipo de ambiente de execução > GPU e reconecte."
        )
    return torch.cuda.get_device_name(0)


def normalize(text):
    return "".join(
        c for c in unicodedata.normalize("NFKD", str(text).lower())
        if not unicodedata.combining(c)
    )


def read_jsonl(path):
    result = []
    with Path(path).open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            item = json.loads(line)
            for key in ("id", "category", "prompt", "answer", "expected_keywords"):
                if key not in item:
                    raise ValueError(f"{path}:{n} sem campo {key}")
            result.append(item)
    if not result:
        raise ValueError(f"Dataset vazio: {path}")
    return result


def format_chat(tokenizer, user_prompt):
    return tokenizer.apply_chat_template(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        tokenize=True,
        add_generation_prompt=True,
    )


class SupervisedExamples(Dataset):
    """Loss aplicada apenas na resposta (tokens do prompt recebem -100)."""

    def __init__(self, records, tokenizer, max_length=384):
        self.rows = []
        for item in records:
            prompt_ids = format_chat(tokenizer, item["prompt"])
            target_ids = tokenizer.encode(item["answer"], add_special_tokens=False)
            target_ids += [tokenizer.eos_token_id]
            if len(prompt_ids) + len(target_ids) > max_length:
                raise ValueError(
                    f"Exemplo {item['id']} possui {len(prompt_ids) + len(target_ids)} "
                    f"tokens; aumente --max-length (atual: {max_length})."
                )
            self.rows.append({
                "input_ids": prompt_ids + target_ids,
                "labels": [-100] * len(prompt_ids) + target_ids,
            })

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        return self.rows[index]


class Collator:
    def __init__(self, tokenizer):
        self.pad_id = tokenizer.pad_token_id

    def __call__(self, features):
        maximum = max(len(row["input_ids"]) for row in features)
        ids = []
        masks = []
        labels = []
        for row in features:
            length = len(row["input_ids"])
            pad = maximum - length
            ids.append(row["input_ids"] + [self.pad_id] * pad)
            masks.append([1] * length + [0] * pad)
            labels.append(row["labels"] + [-100] * pad)
        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "attention_mask": torch.tensor(masks, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }


@torch.inference_mode()
def generate_answer(model, tokenizer, prompt, *, max_new_tokens=180, temperature=0):
    inputs = tokenizer(
        tokenizer.apply_chat_template(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            tokenize=False,
            add_generation_prompt=True,
        ),
        return_tensors="pt",
    ).to(next(model.parameters()).device)
    kwargs = {"max_new_tokens": max_new_tokens, "pad_token_id": tokenizer.eos_token_id}
    if temperature > 0:
        kwargs.update(do_sample=True, temperature=temperature, top_p=0.9)
    else:
        kwargs.update(do_sample=False)
    generated = model.generate(**inputs, **kwargs)
    continuation = generated[0, inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(continuation, skip_special_tokens=True).strip()
