# Auditoria final de entrega — CP2/CP3

**Disciplina:** Generative AI for Engineering  
**Professor:** Francisco Elanio  
**Turma:** 4ESPX  
**Prazo informado:** 15/10/2026, 23h59  
**Repositório público:** https://github.com/GuilhermeSSantos2004/GenerativeAI-Engineering

## Verificação requisito a requisito

| Requisito do enunciado | Status | Evidência no repositório |
|---|---|---|
| Selecionar/escolher LLM | **OK** | `Qwen/Qwen2.5-0.5B-Instruct` em [README](../README.md), [src/common.py](../src/common.py) |
| Problema específico para resolver | **OK** | Diagnóstico e correção de erros Python, [metodologia](METODOLOGIA.md) e [dataset](../data/) |
| Treinar efetivamente uma LLM | **OK** | LoRA supervisionado em [src/train.py](../src/train.py) e [notebook Colab](../notebooks/CP2_CP3_Colab.ipynb); métricas reais [A](../evidences/experiment_a_training.json) e [B](../evidences/experiment_b_training.json) |
| Testar diferentes parâmetros | **OK** | A: LR `2e-4`, rank `8`, 2 épocas; B: LR `5e-5`, rank `16`, 3 épocas; detalhes em [metodologia](METODOLOGIA.md) |
| Verificar/avaliar as respostas | **OK** | 16 casos por variante (48 gerações) em [baseline](../evidences/baseline.json), [LoRA A](../evidences/experiment_a.json), [LoRA B](../evidences/experiment_b.json); [análise de falhas](RESULTADOS_REAIS.md) |
| Testes da LLM usando GPU | **OK** | Treinamentos e avaliações exigem `torch.cuda.is_available()`; [gpu.json](../evidences/gpu.json) registra Tesla T4; [scripts](../src/) e resultados indicam GPU |
| Frontend para criar/inserir prompt | **OK** | [Gradio](../src/ui.py) e [prints reais](../evidences/screenshots/02_frontend_nameerror.png) |
| Print da GPU funcionando no VS Code | **OK com ressalva documental** | [Print real do VS Code](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp): `CUDA disponível: True`, Tesla T4, VRAM e tensor em `cuda:0`; GPU é **remota Colab**, não instalada fisicamente no notebook |
| Toda documentação e código no GitHub | **OK** | README, scripts, notebook, dataset, JSONs, gráficos, capturas, relatório e testes em `main` |
| Grupo de 4 a 5 pessoas | **OK** | [5 integrantes, nomes completos e RMs; turma 4ESPX](GRUPO.md) |

## Detalhes do ambiente

- A GPU é uma **Tesla T4 do Google Colab**; execução do modelo é local ao processo Python nesse servidor, não no hardware físico do computador pessoal.
- PyTorch `2.11.0+cu130`; biblioteca CUDA reportada como `13.0`; `CUDA disponível: True`; tensor real em `cuda:0`.
- O print do VS Code mostra as informações pedidas, mas a **tabela completa do `nvidia-smi` não aparece**; apenas a chamada bem-sucedida `returncode=0`. Nome da GPU, memória e CUDA aparecem diretamente no output do Python.
- As extensões **GPU Environment** e **GPU Monitor** são *sugestões* do enunciado, não requisitos obrigatórios. O projeto comprova a GPU por código no VS Code.

## O que significam os resultados

| Métrica automática nos 16 testes | Baseline | LoRA A | LoRA B |
|---|---:|---:|---:|
| Formato solicitado | 43,75% | 100% | 100% |
| Recall de palavras-chave | 75% | 68,75% | 75% |
| Todos os termos esperados | 56,25% | 50% | 62,5% |

**Interpretação correta:** fine-tuning melhorou o formato; melhora geral na precisão das correções **não está demonstrada**. A revisão qualitativa encontrou falhas verdadeiras em IndexError, AttributeError e outros tipos. Isso está registrado transparentemente em [RESULTADOS_REAIS.md](RESULTADOS_REAIS.md).

## Limitações honestas

1. O conjunto de dados é **sintético e pequeno (128 exemplos)**, com padrões parecidos entre treino, validação e teste. Não demonstra generalização ampla.
2. Os experimentos A e B variam três hiperparâmetros simultaneamente; a comparação não permite atribuir um ganho a apenas um deles.
3. O GitHub guarda **código e métricas reais**, mas os arquivos binários dos adapters LoRA treinados (`adapter_model.safetensors`) foram exportados e preservados no ZIP original do grupo, **não foram adicionados ao GitHub**.
4. O workflow GitHub Actions executa verificações de **integridade/sintaxe em CPU**, enquanto treinamento e avaliações da **LLM** foram realizados na GPU Colab; não confundir verificações de CI com testes de modelo.
5. Uma avaliação perfeita não é alegada: alguns códigos gerados estavam incorretos.

## Conclusão

**Pronto para submissão do LINK do repositório**, pois todos os itens de implementação e evidência do enunciado estão representados e verificáveis. A nota final e a aceitação da GPU remota como evidência de “LLM local” dependem da interpretação do professor. Não há comprovação de entrega efetiva na plataforma acadêmica: o integrante ainda precisa clicar em **Turn in / Entregar**.

**Link para submeter:** https://github.com/GuilhermeSSantos2004/GenerativeAI-Engineering
