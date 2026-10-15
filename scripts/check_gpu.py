"""Exibir e opcionalmente salvar as evidências reais de CUDA / nvidia-smi."""
import argparse
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import torch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_cuda": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(),
        "gpu": [],
    }
    print("Python:", result["python"])
    print("PyTorch:", result["torch"])
    print("CUDA no PyTorch:", result["torch_cuda"])
    print("CUDA disponível:", result["cuda_available"])
    try:
        subprocess.run(["nvidia-smi"], check=False, timeout=20)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("nvidia-smi indisponível")
    if not torch.cuda.is_available():
        raise SystemExit("ERRO: nenhum dispositivo CUDA ativo. Selecione GPU no Colab.")
    for i in range(torch.cuda.device_count()):
        p = torch.cuda.get_device_properties(i)
        item = {
            "index": i,
            "name": p.name,
            "total_memory_gb": round(p.total_memory / (1024 ** 3), 2),
        }
        result["gpu"].append(item)
        print("GPU", i, ":", item)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("Evidência JSON salva em:", path)


if __name__ == "__main__":
    main()
