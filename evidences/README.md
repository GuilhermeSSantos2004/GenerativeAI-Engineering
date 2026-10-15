# Evidências do CP2/CP3

Este diretório será preenchido **somente após executar GPU, treino e avaliações reais**.

O comando `python scripts/export_evidence.py --strict` copia os resultados:
`gpu.json`, `baseline.json`, `experiment_a.json`, `experiment_b.json`,
`comparison.csv`, `comparison.png`, históricos e métricas dos treinamentos.

O comando `python scripts/build_markdown_report.py` gera
`RELATORIO_EXECUCAO.md` com parâmetros e métricas extraídos de arquivos reais.

Crie manualmente `screenshots/gpu_vscode.png` e outras evidências visuais.
A pasta vazia de screenshots não é versionada pelo Git.

**Status inicial:** código preparado, experimentos GPU/prints ainda não executados/publicados.
