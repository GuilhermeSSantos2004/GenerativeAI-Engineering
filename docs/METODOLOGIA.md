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

## Experimentos propostos

| Variante | Learning rate | Épocas | LoRA r | Batch | Acúmulo | Seed |
|---|---:|---:|---:|---:|---:|---:|
| Baseline (sem treino) | — | — | — | — | — | — |
| A | 2e-4 | 2 | 8 | 2 | 4 | 42 |
| B | 5e-5 | 3 | 16 | 2 | 4 | 42 |

A e B **variam três parâmetros conjuntamente**. Sua comparação é exploratória e não isola o efeito causal de um hiperparâmetro. Se houver recursos, repetir mudando apenas uma variável por vez.

## Avaliação

As 16 perguntas reservadas são respondidas com temperatura = 0 por todas as variantes na **GPU**. Medidas:

1. `format_rate`: fração de respostas com os três títulos solicitados;
2. `keyword_recall`: proporção média de termos esperados por exemplo;
3. `full_keyword_rate`: fração de respostas contendo todos os termos esperados;
4. `mean_latency_seconds`: tempo médio por resposta.

**Importante:** palavras-chave podem aparecer em uma resposta semanticamente errada. Cada JSON inclui prompt, resposta de referência, geração real, pontuação e tempo para permitir auditoria. Revisar manualmente correções e possíveis respostas alucinadas.

Também registramos loss de treino/validação, versão CUDA, GPU, VRAM pico, tempo e hiperparâmetros. Nenhuma dessas medições foi preenchida artificialmente no repositório.

## Critérios de conclusão

Projeto só estará completamente evidenciado depois de:
- GPU CUDA disponível e screenshot verdadeiro dentro do VS Code;
- baseline, treinamento A/B e inferências na GPU;
- métricas e adapters salvos;
- comparação e revisão manual das respostas;
- evidências reais versionadas/publicadas no GitHub.
