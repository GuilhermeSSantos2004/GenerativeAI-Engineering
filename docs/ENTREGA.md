# Entrega — CP2/CP3 Generative AI for Engineering

**Turma:** 4ESPX  
**Professor:** Francisco Elanio  
**Data prevista:** 15/10/2026, às 23h59

## Arquivos e evidências do projeto

| Conteúdo | Localização |
|---|---|
| Integrantes e RMs | [docs/GRUPO.md](GRUPO.md) |
| Definição do problema e escolha do modelo | [README](../README.md) e [metodologia](METODOLOGIA.md) |
| Código para treinamento LoRA | [src/train.py](../src/train.py) |
| Notebook do Google Colab | [CP2_CP3_Colab.ipynb](../notebooks/CP2_CP3_Colab.ipynb) |
| Hiperparâmetros e métricas reais | [evidences/](../evidences/) |
| Avaliação e exemplos de respostas | [docs/RESULTADOS_REAIS.md](RESULTADOS_REAIS.md) |
| Frontend para inserir prompts | [src/ui.py](../src/ui.py) |
| Captura da GPU no VS Code | [10_gpu_vscode_tesla_t4.webp](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp) |
| Testes de integridade do dataset | [tests/test_project.py](../tests/test_project.py) |

## Capturas dos testes

![GPU Tesla T4 verificada dentro do VS Code](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp)

[Imagem do VS Code](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp) · [Treinamento A](../evidences/screenshots/06_treinamento_lora_A_t4.png) · [Treinamento B](../evidences/screenshots/07_treinamento_lora_B_t4.png) · [Comparação](../evidences/screenshots/01_colab_comparacao_e_gpu_t4.png) · [Frontend](../evidences/screenshots/02_frontend_nameerror.png)

## Resumo

Foram realizados dois fine-tunings LoRA da Qwen2.5-0.5B-Instruct na GPU Tesla T4 do Colab, além da avaliação do modelo original. A aplicação Gradio permite fornecer um erro Python e visualizar a correção sugerida. Os testes registram ganhos na estrutura das respostas e limitações técnicas na correção de alguns casos.

O ambiente utiliza **GPU remota**, conectada ao VS Code. O código, os dados, os resultados e as capturas estão documentados neste repositório.

**Link da entrega:** https://github.com/GuilhermeSSantos2004/GenerativeAI-Engineering
