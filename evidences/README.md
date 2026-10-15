# Evidências do CP2/CP3 — turma 4ESPX

## Dados de execução GPU já publicados neste GitHub

- [gpu.json](gpu.json): identificação real da Tesla T4, CUDA e PyTorch.
- [experiment_a_training.json](experiment_a_training.json): hiperparâmetros e perdas reais do fine-tuning A.
- [experiment_b_training.json](experiment_b_training.json): hiperparâmetros e perdas reais do fine-tuning B.
- [comparison.csv](comparison.csv): métricas do baseline, LoRA A e LoRA B sobre os 16 testes.
- [comparison.svg](comparison.svg): gráfico refeito com os dados reais do CSV.

A análise das saídas do ZIP está registrada em [docs/RESULTADOS_REAIS.md](../docs/RESULTADOS_REAIS.md). Não confunda métricas automáticas baseadas em palavras-chave com taxa de acertos de código.

## Capturas reais publicadas e verificadas no GitHub

O estudante enviou os seguintes prints em 15/10/2026 e os oito arquivos PNG **originais** foram publicados em [`evidences/screenshots/`](screenshots/) no commit [`0a219b1`](https://github.com/GuilhermeSSantos2004/GenerativeAI-Engineering/commit/0a219b14d44284f2505dfc754eb241b1016ec0ab). Cada arquivo foi conferido diretamente na API do GitHub, com o mesmo tamanho em bytes do arquivo recebido:

| Arquivo | Conteúdo | Análise |
|---|---|---|
| `screenshots/01_colab_comparacao_e_gpu_t4.png` | Comparação dos três modelos e painel T4 no navegador | Suporta uso da GPU e métricas |
| `screenshots/02_frontend_nameerror.png` | Gradio: NameError com solução executável | Resposta coerente |
| `screenshots/03_frontend_indexerror_correcao_incorreta.png` | Gradio: IndexError | Diagnóstico correto, código sugerido usa `números` e `numeros` de forma inconsistente |
| `screenshots/04_frontend_zero_division.png` | Gradio: ZeroDivisionError | Verificação do divisor |
| `screenshots/05_frontend_valueerror_resposta_parcial.png` | Gradio: ValueError | Código de saída muda literal; explicação é imprecisa |
| `screenshots/06_treinamento_lora_A_t4.png` | Treinamento A finalizado, Tesla T4 no painel | Returncode 0 |
| `screenshots/07_treinamento_lora_B_t4.png` | Treinamento B finalizado, Tesla T4 no painel | Returncode 0 |
| `screenshots/08_frontend_prompt_adicional.png` | Teste complementar no Gradio | Demonstra interface em operação |

**Conferência:** os oito links acima estão disponíveis no GitHub e foram associados aos arquivos enviados pelo grupo. Os screenshots do navegador não foram rotulados como capturas do VS Code. Não diga que um print está publicado só por constar na tabela.

## Pendências frente ao professor

- [x] Treino LoRA A e B em GPU Tesla T4, arquivos de métricas reais.
- [x] Comparação do modelo original com os fine-tunings.
- [x] Frontend Gradio com respostas registradas em prints.
- [x] Grupo de 5 integrantes, turma 4ESPX, em `docs/GRUPO.md`.
- [ ] **Print da GPU efetivamente dentro do VS Code**. Os prints atuais são do Google Colab no navegador, não substituem o requisito literal.
- [x] Publicar os oito PNGs originais em `screenshots/`.
- [ ] Publicar os JSON detalhados das 16 respostas por variante a partir do pacote entregue (métricas agregadas já publicadas).

## Galeria visual dos prints enviados

![Comparação dos modelos com Tesla T4](screenshots/01_colab_comparacao_e_gpu_t4.png)

![Frontend para correção de erros Python](screenshots/02_frontend_nameerror.png)

![Treinamento LoRA A finalizado](screenshots/06_treinamento_lora_A_t4.png)

![Treinamento LoRA B finalizado](screenshots/07_treinamento_lora_B_t4.png)

**Não publicar os pesos-base do modelo nem afirmar que os prints no navegador são capturas de dentro do VS Code.**
