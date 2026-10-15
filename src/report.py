"""Consolidar os resultados reais (sem números fictícios)."""
import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


FIELDS = ["format_rate", "keyword_recall", "full_keyword_rate"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--inputs", nargs="+", required=True)
    p.add_argument("--output-dir", default="results/summary")
    args = p.parse_args()
    loaded = [json.loads(Path(path).read_text(encoding="utf-8")) for path in args.inputs]
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    labels = [Path(path).stem for path in args.inputs]
    with (out / "comparison.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["run", "variant", "gpu", "sample_count", *FIELDS])
        for label, run in zip(labels, loaded):
            writer.writerow([
                label, run["variant"], run["gpu"], run["sample_count"],
                *[run[field] for field in FIELDS]
            ])
    fig, ax = plt.subplots(figsize=(10, 5))
    width = 0.23
    indexes = list(range(len(labels)))
    for j, field in enumerate(FIELDS):
        x_positions = [x + j * width for x in indexes]
        ax.bar(x_positions, [100 * r[field] for r in loaded],
               width=width, label=field)
    ax.set_xticks([x + width for x in indexes], labels)
    ax.set_ylim(0, 105)
    ax.set_ylabel("Percentual (%)")
    ax.set_title("Avaliação real no conjunto de teste reservado")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "comparison.png", dpi=160)
    plt.close(fig)
    print("Arquivos gerados:", out / "comparison.csv", out / "comparison.png")


if __name__ == "__main__":
    main()
