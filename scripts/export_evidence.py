"""Publica CÓPIAS somente de evidências reais já produzidas no Colab."""
import argparse
import shutil
from pathlib import Path

FILE_MAP = {
    "results/gpu.json": "evidences/gpu.json",
    "results/baseline.json": "evidences/baseline.json",
    "results/experiment_a.json": "evidences/experiment_a.json",
    "results/experiment_b.json": "evidences/experiment_b.json",
    "results/summary/comparison.csv": "evidences/comparison.csv",
    "results/summary/comparison.png": "evidences/comparison.png",
    "outputs/experiment_a/metrics.json": "evidences/experiment_a_training.json",
    "outputs/experiment_a/history.json": "evidences/experiment_a_history.json",
    "outputs/experiment_b/metrics.json": "evidences/experiment_b_training.json",
    "outputs/experiment_b/history.json": "evidences/experiment_b_history.json",
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--strict", action="store_true",
                   help="Falhar se qualquer evidência esperada ainda não existir")
    args = p.parse_args()
    copied = 0
    missing = []
    for source, dest in FILE_MAP.items():
        src = Path(source)
        if not src.is_file():
            missing.append(source)
            continue
        dst = Path(dest)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"{src} -> {dst}")
        copied += 1
    print(f"Copiados: {copied}/{len(FILE_MAP)}")
    if missing:
        print("Ainda faltam evidências reais:")
        for item in missing:
            print(" -", item)
    if args.strict and missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
