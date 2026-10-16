# Checklist de entrega — 15/10/2026 às 23h59

Este checklist foi atualizado após a execução real no Google Colab em 15/10/2026. A disciplina é da turma **4ESPX**; a equipe tem cinco integrantes confirmados. Os experimentos GPU e a captura no VS Code foram concluídos e publicados. A GPU exibida é remota, fornecida pelo Google Colab.

| Item do professor | Implementação no repositório | Evidência a obter |
|---|---|---|
| Selecionar LLM | Qwen2.5-0.5B-Instruct | Executado na GPU Tesla T4 |
| Problema específico | Diagnóstico de erros Python | Testes e screenshots Gradio recebidos |
| Treinar LLM | `src/train.py` + notebook | Concluído A e B, metrics.json publicado |
| Testar parâmetros | experimentos A/B | Concluído, ranks/LR/épocas registrados |
| Avaliar respostas | `src/evaluate.py` | Concluído (16 casos cada); JSONs completos publicados em `evidences/` |
| Testes com GPU | `require_gpu()` impede CPU | Tesla T4 confirmada em `evidences/gpu.json` e no VS Code; execução de nvidia-smi terminou com `returncode=0` (tabela não visível na captura) |
| Frontend | `src/ui.py` (Gradio) | Testado com prompts reais; os nove prints originais estão publicados no GitHub |
| Print da GPU no VS Code | [`10_gpu_vscode_tesla_t4.webp`](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp) | **CONCLUÍDO**: CUDA True, Tesla T4, VRAM e tensor cuda:0 visíveis no VS Code |
| Documentação e código no GitHub | README, docs, fontes, dataset, notebook | commit dos resultados |
| Grupo de 4 a 5 pessoas | `docs/GRUPO.md` | Confirmados 5 integrantes com nomes completos e RMs, turma 4ESPX |

## Prints efetivamente publicados (nomes exatos)

1. [GPU CUDA e Tesla T4 dentro do VS Code](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp) — mostra `CUDA disponível: True`, VRAM 14,56 GiB e tensor em `cuda:0`; `nvidia-smi` finalizou com retorno zero, mas a tabela do comando não foi exibida por inteiro.
2. [Treinamento LoRA A](../evidences/screenshots/06_treinamento_lora_A_t4.png) — execução encerrada com sucesso no Colab.
3. [Treinamento LoRA B](../evidences/screenshots/07_treinamento_lora_B_t4.png) — execução encerrada com sucesso no Colab.
4. [Comparação original vs LoRA A/B](../evidences/screenshots/01_colab_comparacao_e_gpu_t4.png) — métricas e painel T4.
5. [Frontend Gradio — caso NameError](../evidences/screenshots/02_frontend_nameerror.png) — prompt e resposta.
6. [Frontend Gradio — caso IndexError](../evidences/screenshots/03_frontend_indexerror_correcao_incorreta.png) — registra também um erro real na correção.

[Confira todos os 10 screenshots](../evidences/screenshots/). Os prints do navegador Colab são identificados como navegador e a captura obrigatória do editor é realmente do VS Code.

## Auditoria de capturas recebidas em 15/10/2026

- Comparação de baseline/A/B no Google Colab + painel Tesla T4: recebida.
- LoRA A finalizado sem erro visível (returncode=0) e painel Tesla T4: recebida.
- LoRA B finalizado sem erro visível (returncode=0) e painel Tesla T4: recebida.
- Gradio: NameError, IndexError, ZeroDivisionError, ValueError, caso adicional: recebidos.
- **Atenção:** no caso IndexError a solução sugerida usa nomes de variáveis inconsistentes, logo não é evidência de correção perfeita.
- Print de CUDA no **VS Code**, como enunciado pede: **recebido e publicado** no commit [`5fb9163`](https://github.com/GuilhermeSSantos2004/GenerativeAI-Engineering/commit/5fb9163f3871f5c57367d7f0fc25aba15a93298b). A saída do VS Code registra PyTorch 2.11.0+cu130, CUDA 13.0, Tesla T4, 14.56 GiB de VRAM, tensor em cuda:0 e `returncode=0` de nvidia-smi.

Os **nove PNGs originais foram publicados e verificados** em [`evidences/screenshots/`](../evidences/screenshots/) por meio do commit [`0a219b1`](https://github.com/GuilhermeSSantos2004/GenerativeAI-Engineering/commit/0a219b14d44284f2505dfc754eb241b1016ec0ab). Os JSONs completos das 48 respostas (16 perguntas × 3 variantes), as métricas, os históricos e os gráficos de loss foram publicados na pasta [`evidences`](../evidences/). Veja [o inventário das evidências](../evidences/README.md).
