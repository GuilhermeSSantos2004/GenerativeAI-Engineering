# Checklist de entrega — 15/10/2026 às 23h59

Este checklist distingue **código já preparado** de **evidência experimental ainda exigida**.

| Item do professor | Implementação no repositório | Evidência a obter |
|---|---|---|
| Selecionar LLM | Qwen2.5-0.5B-Instruct | modelo executando na GPU |
| Problema específico | Diagnóstico de erros Python | prompts de demonstração |
| Treinar LLM | `src/train.py` + notebook | pesos LoRA, logs e métricas reais |
| Testar parâmetros | experimentos A/B | loss e comparação geradas |
| Avaliar respostas | `src/evaluate.py` | saídas de 16 testes por variante |
| Testes com GPU | `require_gpu()` impede CPU | `gpu.json` e `nvidia-smi` |
| Frontend | `src/ui.py` (Gradio) | screenshot interagindo |
| Print da GPU no VS Code | instruções em `EXECUCAO.md` | print original do editor |
| Documentação e código no GitHub | README, docs, fontes, dataset, notebook | commit dos resultados |
| Grupo de 4 a 5 pessoas | `docs/GRUPO.md` | conferir integrantes e RMs |

## Prints recomendados

- `evidences/screenshots/gpu_vscode.png`: VS Code com notebook Colab, CUDA, dispositivo e nvidia-smi.
- `evidences/screenshots/treinamento_a.png`: loss e treino A funcionando.
- `evidences/screenshots/treinamento_b.png`: loss e treino B funcionando.
- `evidences/screenshots/comparacao.png`: tabela ou gráfico comparativo real.
- `evidences/screenshots/frontend.png`: prompt digitado no Gradio e resposta real.

**Nunca** preencha métricas inventadas ou prints de terceiros para simular a execução. Guarde também o ZIP dos adapters fora do Colab.
