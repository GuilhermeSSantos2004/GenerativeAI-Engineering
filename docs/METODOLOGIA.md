# Metodologia — CP2/CP3

## Problema específico

Explicar a causa de exceções Python e propor correção curta e verificável.
Entradas: trecho de código + erro observado. Saídas: três seções em português:
**Causa**, **Correção**, **Código corrigido**.

## Modelo e treinamento

- Modelo: `Qwen/Qwen2.5-0.5B-Instruct`.
- Pesos de código aberto executados diretamente na GPU do runtime (sem API externa para inferência).
- Fine-tuning supervisionado com **LoRA** nas projeções de atenção `q_proj` e `v_proj`. Os pesos-base permanecem congelados.
- Alvo do treinamento: a loss calcula gradiente **somente nos tokens da resposta**. O prompt recebe labels `-100`.
- Precisão: FP16 ou BF16 dependendo da GPU. Treinamento interrompe se CUDA não estiver disponível.
- Semente: 42. Dependendo do hardware, versões CUDA e paralelismo, reprodutibilidade bit a bit não é garantida.

## Dados

Dataset sintético criado especificamente para a disciplina, sem informações pessoais nem código corporativo:

| Split | Exemplos | Uso |
|---|---:|---|
| `data/train.jsonl` | 96 | Ajuste LoRA |
| `data/val.jsonl` | 16 | Validação, escolha de melhor checkpoint |
| `data/test.jsonl` | 16 | Comparação final, sem treino |

16 famílias de problemas: NameError (variável e função), TypeError (concatenação, argumento ausente, None e iterabilidade), ZeroDivisionError, IndexError, KeyError, AttributeError, ValueError, SyntaxError, IndentationError, FileNotFoundError, UnboundLocalError, ModuleNotFoundError.

IDs e prompts exatos são exclusivos por split. Contudo, **os casos seguem os mesmos padrões de erro**, com variações de parâmetros e nomes. Isso facilita observar especialização, mas **limita alegações de generalização**. Não use estas métricas como prova de aptidão para depurar código arbitrário.

## Experimentos realizados

| Variante | Learning rate | Épocas | LoRA r | Batch | Acúmulo | Seed |
|---|---:|---:|---:|---:|---:|---:|
| Baseline (sem treino) | — | — | — | — | — | — |
| A | 2e-4 | 2 | 8 | 2 | 4 | 42 |
| B | 5e-5 | 3 | 16 | 2 | 4 | 42 |

As configurações A e B alteram rank LoRA, learning rate e número de épocas. A comparação permite observar diferenças entre configurações, mas não isola o efeito de cada hiperparâmetro.

## Avaliação

As 16 perguntas reservadas são respondidas com temperatura = 0 por todas as variantes na **GPU**. Medidas:

1. `format_rate`: fração de respostas com os três títulos solicitados;
2. `keyword_recall`: proporção média de termos esperados por exemplo;
3. `full_keyword_rate`: fração de respostas contendo todos os termos esperados;
4. `mean_latency_seconds`: tempo médio por resposta.

A presença de palavras-chave não significa, necessariamente, que a correção do código esteja certa. Por isso, os arquivos JSON guardam o prompt, a referência, a resposta gerada, a pontuação e o tempo. A discussão dos casos em que o modelo errou está em [Resultados dos experimentos](RESULTADOS_REAIS.md).

Também foram registrados loss de treinamento e validação, versão CUDA, modelo da GPU, uso de memória, duração e hiperparâmetros.

## Reprodutibilidade e limitações

Os scripts e o notebook estão disponíveis neste repositório, junto dos resultados da execução com Tesla T4. O ambiente gratuito do Colab pode atribuir outra GPU e versões de biblioteca diferentes, o que pode afetar tempo e resultados.

O dataset sintético possui padrões parecidos entre os conjuntos e foi pensado para uma atividade acadêmica, não para uma solução pronta para produção. Seria interessante ampliar o número de exemplos, incluir erros de projetos reais e avaliar as correções executando testes Python automaticamente.

**Evidências:** [GPU no VS Code](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp) · [Avaliações completas](../evidences/) · [Gráficos e resultados](RESULTADOS_REAIS.md)
