# Conferência dos requisitos — CP2/CP3

**Disciplina:** Generative AI for Engineering  
**Professor:** Francisco Elanio  
**Turma:** 4ESPX  
**Entrega:** 15/10/2026

## Correspondência entre atividade e projeto

| Item solicitado | Como foi realizado | Evidência |
|---|---|---|
| Escolha da LLM | Qwen2.5-0.5B-Instruct | [Código](../src/common.py) |
| Problema específico | Diagnosticar erros Python e propor correções em português | [Metodologia](METODOLOGIA.md) |
| Treinamento da LLM | Fine-tuning supervisionado LoRA | [Notebook](../notebooks/CP2_CP3_Colab.ipynb), [experimento A](../evidences/experiment_a_training.json) e [B](../evidences/experiment_b_training.json) |
| Hiperparâmetros | Comparação de duas configurações de épocas, learning rate e rank LoRA | [Metodologia](METODOLOGIA.md) |
| Avaliação das respostas | Baseline e duas versões treinadas, com 16 perguntas por modelo | [Resultados](RESULTADOS_REAIS.md), [respostas em JSON](../evidences/) |
| Uso de GPU | Treinamentos e inferências avaliadas na NVIDIA Tesla T4 do Colab | [Dados da GPU](../evidences/gpu.json) |
| Frontend de prompts | Interface Gradio para enviar erros e receber respostas | [Código do frontend](../src/ui.py), [imagem](../evidences/screenshots/02_frontend_nameerror.png) |
| GPU no VS Code | Execução da verificação CUDA no notebook aberto no editor | [Captura de tela](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp) |
| Documentação no GitHub | Código, dados, instruções e resultados experimentais | [Repositório](../README.md) |
| Grupo | Cinco integrantes com seus RMs | [Equipe 4ESPX](GRUPO.md) |

## Ambiente de execução

A execução utilizou o Google Colab com **NVIDIA Tesla T4**, PyTorch `2.11.0+cu130` e CUDA `13.0` reportado pelo PyTorch. A GPU foi utilizada também a partir do VS Code, por conexão ao runtime remoto. O computador pessoal não possui fisicamente essa placa.

O print do editor mostra o nome da GPU, 14,56 GiB de memória, disponibilidade do CUDA e um tensor alocado em `cuda:0`. O comando `nvidia-smi` foi executado com retorno zero, embora sua tabela não esteja visível por inteiro na captura.

## Resultados e discussão

| Métrica nos 16 testes | Modelo original | LoRA A | LoRA B |
|---|---:|---:|---:|
| Resposta no formato esperado | 43,75% | 100% | 100% |
| Recall de termos esperados | 75% | 68,75% | 75% |
| Todos os termos esperados | 56,25% | 50% | 62,5% |

Os dois fine-tunings melhoraram a organização das respostas. As métricas de termos foram mistas e algumas sugestões de código permaneceram incorretas. Essas ocorrências estão descritas no [relatório de resultados](RESULTADOS_REAIS.md).

O conjunto de treino é sintético e pequeno. Além disso, os experimentos alteraram mais de um hiperparâmetro de cada vez, de modo que a comparação entre A e B não identifica isoladamente o efeito de cada variável.

Os scripts e os registros de execução estão no repositório. Os **adaptadores LoRA** foram salvos no ZIP de resultados da execução, separado do controle de versão.

## Arquivos principais

- [README e apresentação](../README.md)
- [Notebook de treinamento](../notebooks/CP2_CP3_Colab.ipynb)
- [Scripts de treinamento e avaliação](../src/)
- [Registros, capturas e gráficos](../evidences/)
- [Orientações de execução](EXECUCAO.md)
