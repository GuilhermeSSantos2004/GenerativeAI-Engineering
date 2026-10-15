"""Relatório em Markdown populado exclusivamente com medições existentes."""
import json
from datetime import datetime, timezone
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def pc(value):
    return f"{100 * value:.2f}%"


def main():
    keys = ["baseline", "experiment_a", "experiment_b"]
    paths = [Path("results") / (k + ".json") for k in keys]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise SystemExit("Faltam avaliações reais: " + ", ".join(missing))
    evals = [load(path) for path in paths]
    settings = [load(Path("outputs") / k / "metrics.json")
                for k in keys[1:]]
    lines = [
        "# Relatório de execução real — CP2/CP3",
        "",
        f"Gerado em UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "> As métricas a seguir foram lidas dos JSON produzidos durante a execução. "
        "Presença de palavras-chave não garante correção técnica da resposta.",
        "",
        "## Hardware e parâmetros",
        "",
        f"- GPU utilizada nas avaliações: {evals[0]['gpu']}",
        "- Modelo base: Qwen/Qwen2.5-0.5B-Instruct",
        f"- Amostras reservadas de teste: {evals[0]['sample_count']}",
        f"- Temperatura da avaliação: {evals[0]['temperature']}",
    ]
    for idx, train in enumerate(settings, 1):
        config = train["config"]
        lines += [
            f"- Experimento {'A' if idx == 1 else 'B'}: "
            f"r={config['lora_r']}, LR={config['learning_rate']}, "
            f"épocas={config['epochs']}, batch={config['batch_size']}, "
            f"acúmulo={config['grad_accum']}, tempo={train['elapsed_seconds']}s, "
            f"pico VRAM={train['max_gpu_memory_gb']} GB, "
            f"eval_loss={train['val_metrics'].get('eval_loss', 'N/D')}"
        ]
    lines += [
        "",
        "## Comparação das respostas (teste reservado)",
        "",
        "| Variante | Estrutura completa | Recall das palavras-chave | Todas palavras-chave | Latência média |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, r in zip(("Base", "LoRA A", "LoRA B"), evals):
        lines.append(
            f"| {label} | {pc(r['format_rate'])} | {pc(r['keyword_recall'])} | "
            f"{pc(r['full_keyword_rate'])} | {r['mean_latency_seconds']:.3f}s |"
        )
    lines.extend([
        "",
        "## Respostas efetivamente geradas (mesmas entradas)",
        "",
    ])
    for case_index in (0, 1, 2):
        sample = evals[0]["examples"][case_index]
        lines.extend([
            f"### Caso {case_index + 1} — {sample['id']}",
            "",
            "**Prompt avaliado:**",
            "",
            "~~~text", sample["prompt"], "~~~", "",
        ])
        for label, r in zip(("Base", "LoRA A", "LoRA B"), evals):
            item = r["examples"][case_index]
            if item["id"] != sample["id"]:
                raise ValueError("Os resultados não têm a mesma ordem de teste")
            lines.extend([
                f"**{label}:**",
                "",
                "~~~text", item["generated_answer"], "~~~", "",
            ])
    lines.extend([
        "## Limitações e validação manual",
        "",
        "- Os casos foram gerados sinteticamente e têm semelhanças de padrão entre os splits.",
        "- As métricas automáticas medem estrutura e termos esperados, não a execução "
        "segura do código sugerido.",
        "- Revisar manualmente as respostas de cada categoria, identificando falsos acertos "
        "e sugestões incorretas antes de concluir sobre superioridade do modelo.",
        "- Não houve avaliação humana cega por múltiplos avaliadores nesta coleta.",
    ])
    out = Path("evidences/RELATORIO_EXECUCAO.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Relatório preenchido com dados reais:", out)


if __name__ == "__main__":
    main()
