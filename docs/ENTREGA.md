# Checklist de entrega — 15/10/2026 às 23h59

Este checklist foi atualizado após a execução real no Google Colab em 15/10/2026. A disciplina é da turma **4ESPX**; a equipe tem cinco integrantes confirmados. Diferencie **treino concluído** de **print no VS Code ainda pendente**.

| Item do professor | Implementação no repositório | Evidência a obter |
|---|---|---|
| Selecionar LLM | Qwen2.5-0.5B-Instruct | Executado na GPU Tesla T4 |
| Problema específico | Diagnóstico de erros Python | Testes e screenshots Gradio recebidos |
| Treinar LLM | `src/train.py` + notebook | Concluído A e B, metrics.json publicado |
| Testar parâmetros | experimentos A/B | Concluído, ranks/LR/épocas registrados |
| Avaliar respostas | `src/evaluate.py` | Concluído (16 casos cada); JSONs completos publicados em `evidences/` |
| Testes com GPU | `require_gpu()` impede CPU | Tesla T4 confirmada em `evidences/gpu.json`; print nvidia-smi no VS Code ainda pendente |
| Frontend | `src/ui.py` (Gradio) | Testado com prompts reais; os nove prints originais estão publicados no GitHub |
| Print da GPU no VS Code | instruções em `EXECUCAO.md` | **PENDENTE**: prints atuais são do navegador Colab |
| Documentação e código no GitHub | README, docs, fontes, dataset, notebook | commit dos resultados |
| Grupo de 4 a 5 pessoas | `docs/GRUPO.md` | Confirmados 5 integrantes, turma 4ESPX; conferir se RMs continuam iguais |

## Prints recomendados

- `evidences/screenshots/gpu_vscode.png`: VS Code com notebook Colab, CUDA, dispositivo e nvidia-smi.
- `evidences/screenshots/treinamento_a.png`: loss e treino A funcionando.
- `evidences/screenshots/treinamento_b.png`: loss e treino B funcionando.
- `evidences/screenshots/comparacao.png`: tabela ou gráfico comparativo real.
- `evidences/screenshots/frontend.png`: prompt digitado no Gradio e resposta real.

**Nunca** preencha métricas inventadas ou prints de terceiros para simular a execução. Guarde também o ZIP dos adapters fora do Colab.


## Auditoria de capturas recebidas em 15/10/2026

- Comparação de baseline/A/B no Google Colab + painel Tesla T4: recebida.
- LoRA A finalizado sem erro visível (returncode=0) e painel Tesla T4: recebida.
- LoRA B finalizado sem erro visível (returncode=0) e painel Tesla T4: recebida.
- Gradio: NameError, IndexError, ZeroDivisionError, ValueError, caso adicional: recebidos.
- **Atenção:** no caso IndexError a solução sugerida usa nomes de variáveis inconsistentes, logo não é evidência de correção perfeita.
- Print de CUDA no **VS Code**, como enunciado pede: **ainda não recebido**.

Os **nove PNGs originais foram publicados e verificados** em [`evidences/screenshots/`](../evidences/screenshots/) por meio do commit [`0a219b1`](https://github.com/GuilhermeSSantos2004/GenerativeAI-Engineering/commit/0a219b14d44284f2505dfc754eb241b1016ec0ab). Os JSONs completos das 48 respostas (16 perguntas × 3 variantes), as métricas, os históricos e os gráficos de loss foram publicados na pasta [`evidences`](../evidences/). Veja [o inventário das evidências](../evidences/README.md).
