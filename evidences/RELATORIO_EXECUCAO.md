# Relatório de execução real — CP2/CP3

Gerado em UTC: 2026-10-15T21:54:25.202629+00:00

> As métricas a seguir foram lidas dos JSON produzidos durante a execução. Presença de palavras-chave não garante correção técnica da resposta.

## Hardware e parâmetros

- GPU utilizada nas avaliações: Tesla T4
- Modelo base: Qwen/Qwen2.5-0.5B-Instruct
- Amostras reservadas de teste: 16
- Temperatura da avaliação: 0.0
- Experimento A: r=8, LR=0.0002, épocas=2.0, batch=2, acúmulo=4, tempo=56.87s, pico VRAM=3.613 GB, eval_loss=0.6999666690826416
- Experimento B: r=16, LR=5e-05, épocas=3.0, batch=2, acúmulo=4, tempo=91.37s, pico VRAM=3.622 GB, eval_loss=0.790817379951477

## Comparação das respostas (teste reservado)

| Variante | Estrutura completa | Recall das palavras-chave | Todas palavras-chave | Latência média |
|---|---:|---:|---:|---:|
| Base | 43.75% | 75.00% | 56.25% | 3.162s |
| LoRA A | 100.00% | 68.75% | 50.00% | 2.061s |
| LoRA B | 100.00% | 75.00% | 62.50% | 2.411s |

## Respostas efetivamente geradas (mesmas entradas)

### Caso 1 — NameError-7

**Prompt avaliado:**

~~~text
Resolva o erro abaixo em Python.
Código:
```python
print(total_7)
```
Erro observado: NameError: name 'total_7' is not defined
Responda com Causa, Correção e Código corrigido.
~~~

**Base:**

~~~text
Causa: O nome "total_7" não foi definido antes da chamada ao método print.

Correção:

```python
def total_7():
    return 7

print(total_7())
```

Este código define uma função chamada `total_7` que retorna o valor 7. Depois, chama essa função para imprimir o resultado.
~~~

**LoRA A:**

~~~text
Causa: o valor da variável total_7 não foi definido antes.
Correção: declarar a variável antes do print.
Código corrigido:
```python
total_7 = 0
print(total_7)
```
~~~

**LoRA B:**

~~~text
Causa: A variável `total_7` não foi definida antes da chamada do método `print`.
Correção: Defina a variável antes da chamada do método `print`.
Código corrigido:
```python
def total_7():
    return 7

print(total_7())
```
~~~

### Caso 2 — TypeError_concat-7

**Prompt avaliado:**

~~~text
Resolva o erro abaixo em Python.
Código:
```python
idade_7 = 27
print("Idade: " + idade_7)
```
Erro observado: TypeError: can only concatenate str (not "int") to str
Responda com Causa, Correção e Código corrigido.
~~~

**Base:**

~~~text
Causa: O erro ocorre porque as variáveis `idade_7` e `idade_10` são convertidas para inteiros antes de serem concatenadas.

Correção:

```python
idade_10 = 35
idade_7 = 27
print(f"Idade: {idade_7}")
print(f"Idade: {idade_10}")
```

Código corrigido:

```python
idade_10 = 35
idade_7 = 27
print(f"Idade: {idade_7}")
print(f"Idade: {idade_10}")
```
~~~

**LoRA A:**

~~~text
Causa: o tipo int não pode ser concatenado com str.
Correção: use str para concatenar.
Código corrigido:
```python
idade_7 = 27
print(f"Idade: {idade_7}")
```
~~~

**LoRA B:**

~~~text
Causa: O tipo int não pode ser concatenado com str.
Correção: Use str para concatenar.
Código corrigido:
```python
idade_7 = 27
print(f"Idade: {idade_7}")
```
~~~

### Caso 3 — ZeroDivisionError-7

**Prompt avaliado:**

~~~text
Resolva o erro abaixo em Python.
Código:
```python
total = 107
divisor = 0
print(total / divisor)
```
Erro observado: ZeroDivisionError: division by zero
Responda com Causa, Correção e Código corrigido.
~~~

**Base:**

~~~text
Causa: Divisão por zero ocorreu porque o divisor (0) foi usado na divisão.

Correção:

```python
total = 107
divisor = 0
if divisor != 0:
    print(total / divisor)
else:
    print("Divisor cannot be zero.")
```

Este código verifica se o divisor é diferente de zero antes de realizar a divisão, garantindo que o programa não execute com exceções desnecessárias.
~~~

**LoRA A:**

~~~text
Causa: divisão por zero
Correção: verifique se o divisor for zero antes da divisão
Código corrigido:
```python
total = 107
if divisor == 0:
    print("Divisão por zero")
else:
    print(total / divisor)
```
~~~

**LoRA B:**

~~~text
Causa: divisão por zero
Correção: verifique se o divisor for zero antes da divisão
Código corrigido:
```python
total = 107
if divisor == 0:
    print("Divisão por zero")
else:
    print(total / divisor)
```
~~~

## Limitações e validação manual

- Os casos foram gerados sinteticamente e têm semelhanças de padrão entre os splits.
- As métricas automáticas medem estrutura e termos esperados, não a execução segura do código sugerido.
- Revisar manualmente as respostas de cada categoria, identificando falsos acertos e sugestões incorretas antes de concluir sobre superioridade do modelo.
- Não houve avaliação humana cega por múltiplos avaliadores nesta coleta.
