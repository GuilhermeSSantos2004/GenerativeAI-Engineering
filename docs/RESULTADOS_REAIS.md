# Resultados reais — execução de 15/10/2026

Os dados deste relatório foram obtidos no treinamento realizado em 15/10/2026 com a GPU Tesla T4 do Google Colab. O conjunto de resultados inclui os [arquivos JSON das respostas](../evidences/), os históricos de treinamento e a [captura do VS Code](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp).

## Hardware e execução

- GPU: NVIDIA Tesla T4; memória total reportada: **14,56 GiB**.
- PyTorch: `2.11.0+cu130`; CUDA reportado pelo PyTorch: **13.0**.
- `cuda_available: true` registrado pelo script `scripts/check_gpu.py`.
- Modelo base: `Qwen/Qwen2.5-0.5B-Instruct`.
- Dataset: 96 exemplos de treino, 16 de validação e 16 reservados para teste.
- Treinamento supervisionado LoRA: dois adapters exportados, A com rank 8 e B com rank 16.

| Parâmetro | Experimento A | Experimento B |
|---|---:|---:|
| Learning rate | 0.0002 | 0.00005 |
| Épocas | 2 | 3 |
| Batch size | 2 | 2 |
| Acúmulo de gradiente | 4 | 4 |
| LoRA rank | 8 | 16 |
| Seed | 42 | 42 |
| Tempo total reportado | **56,87 s** | **91,37 s** |
| Train loss | 0,813971 | 0,872740 |
| Validation loss | 0,699967 | 0,790817 |
| Pico de memória CUDA alocada | 3,613 GiB | 3,622 GiB |

As perdas pertencem a execuções com **quantidades diferentes de épocas e hiperparâmetros**; não permitem comparação causal simples. Não houve investigação de variância entre múltiplas seeds.

## Avaliação no mesmo conjunto de teste (16 exemplos)

| Métrica automática | Modelo original | LoRA A | LoRA B |
|---|---:|---:|---:|
| Taxa de resposta com os três títulos esperados | **43,75%** | **100,00%** | **100,00%** |
| Recall médio de palavras-chave | **75,00%** | **68,75%** | **75,00%** |
| Respostas com todas palavras-chave esperadas | **56,25%** | **50,00%** | **62,50%** |
| Latência média reportada por resposta | **3,162 s** | **2,061 s** | **2,411 s** |

### Interpretação

- O fine-tuning melhorou claramente a **aderência ao formato** solicitado, com 100% em A e B contra 43,75% no baseline.
- A configuração B teve maior taxa de presença de todos os termos (62,5%), mas **não superou o recall médio de palavras-chave do modelo original** (ambos 75%).
- O experimento A ficou abaixo do baseline nas duas métricas de termos.
- **Esses percentuais NÃO medem o acerto técnico do código**, apenas características textuais das respostas.

## Auditoria qualitativa: limitações concretas das respostas geradas

Algumas saídas do arquivo [`evidences/experiment_b.json`](../evidences/experiment_b.json) demonstram que **formato correto não é igual a código executável correto**:

1. **IndexError-7:** o modelo B sugere alterar uma variável com nome acentuado (`números`) e depois acessar `numeros[11]`; essa proposta pode gerar `NameError` e não resolve de forma válida o índice fora do intervalo.
2. **AttributeError-7:** apesar de mencionar que `None` não tem `strip()`, o código que sugere contém novamente `texto = None; print(texto.strip())`, reproduzindo o erro original.
3. **TypeError_missing_arg-7:** o modelo B trata equivocadamente o segundo argumento obrigatório de `somar(a, b)` como problema de tipos/listas, confundindo a causa principal.
4. **TypeError_None-7:** a correção sugerida converte para string e trata a operação como concatenação, desviando da intenção original de somar valores numéricos.

O experimento A também erra a correção de **AttributeError-7**, repetindo `texto.strip()` quando o objeto é `None`. Esse é um alerta de que o treinamento com dataset sintético pequeno melhorou o formato de saída, **sem garantir confiabilidade técnica**.

## Conclusão baseada nos dados disponíveis

O projeto implementa e executa fine-tuning LoRA verdadeiro em GPU CUDA com dois conjuntos de hiperparâmetros. A comparação mostra ganho robusto em **estrutura** de resposta e resultados mistos em **presença de palavras-chave**. Não há evidência suficiente para afirmar melhora geral no diagnóstico correto de erros Python. Recomenda-se mais dados reais e variados, validação executável das correções, anotação humana e treino/teste com padrões distintos.

## Arquivos e próximos aprimoramentos

Os [resultados completos](../evidences/), as [imagens do treinamento e da interface](../evidences/screenshots/) e a [lista dos integrantes](GRUPO.md) estão disponíveis neste repositório. Os arquivos dos adaptadores LoRA (`adapter_model.safetensors`) foram exportados no ZIP de resultados, mantido separadamente.

Como continuidade, seria útil treinar com mais exemplos de problemas reais, executar testes automatizados sobre o código sugerido e comparar hiperparâmetros alterando apenas uma variável por experimento. Essas mudanças permitiriam medir a evolução do modelo com mais segurança.
