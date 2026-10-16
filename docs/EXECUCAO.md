# Execução no Google Colab Free + VS Code

## 1. Colab com GPU

1. Acesse [o notebook do projeto](https://colab.research.google.com/github/GuilhermeSSantos2004/GenerativeAI-Engineering/blob/main/notebooks/CP2_CP3_Colab.ipynb).
2. Faça login na sua conta Google.
3. Clique em **Ambiente de execução > Alterar o tipo de ambiente de execução > Acelerador de hardware: GPU**.
4. Execute as células **em ordem**, uma de cada vez.
5. A primeira célula testa um tensor real `cuda:0` e exibe `nvidia-smi`. Sem GPU, o fluxo para.
6. A célula de instalação clona/atualiza o repositório e instala dependências.
7. Na avaliação baseline e nos treinos A/B, observe logs e GPU.
8. Ao final, exporte os JSON, CSV, PNG, relatório, adapters e baixe o ZIP **antes do Colab expirar**.
9. O servidor Gradio é aberto na última célula. `--share` cria URL temporária pública: **não coloque informações confidenciais**.

A disponibilidade de GPU e a duração das sessões variam no Colab Free. Se o ambiente estiver sem CUDA, escolha outro runtime com GPU e execute a verificação novamente.

## 2. VS Code conectado ao Colab

A extensão [Google Colab para VS Code](https://marketplace.visualstudio.com/items?itemName=Google.colab) permite abrir o notebook `.ipynb` no editor e executar suas células em um runtime do Colab. Basta selecionar o kernel `Colab` e conectar a um ambiente com GPU.

Para conferir o ambiente, execute a primeira célula do notebook. Ela imprime a versão do PyTorch, a disponibilidade do CUDA, o modelo da GPU, a VRAM e o dispositivo usado por um tensor de teste.

![Execução da verificação de GPU no VS Code](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp)

[Ver a captura em tamanho original](../evidences/screenshots/10_gpu_vscode_tesla_t4.webp)

Na execução registrada neste projeto, o dispositivo era uma **Tesla T4 do Google Colab** (GPU remota), com `CUDA disponível: True` e tensor em `cuda:0`.

## 3. Execução via terminal conectado a GPU

No diretório do repositório, em ambiente com PyTorch CUDA:

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests
python scripts/check_gpu.py --output results/gpu.json
python -m src.evaluate --output results/baseline.json
python -m src.train --output-dir outputs/experiment_a --learning-rate 0.0002 --epochs 2 --lora-r 8
python -m src.evaluate --adapter outputs/experiment_a/final_adapter --output results/experiment_a.json
python -m src.train --output-dir outputs/experiment_b --learning-rate 0.00005 --epochs 3 --lora-r 16
python -m src.evaluate --adapter outputs/experiment_b/final_adapter --output results/experiment_b.json
python -m src.report --inputs results/baseline.json results/experiment_a.json results/experiment_b.json
python scripts/export_evidence.py --strict
python scripts/build_markdown_report.py
python -m src.ui --adapter outputs/experiment_a/final_adapter
```

Para frontend em Colab, use `python -m src.ui --adapter outputs/experiment_a/final_adapter --share`. Fora do Colab, abra http://localhost:7860.

O Transformers baixa o modelo-base público quando necessário. Os adaptadores LoRA são salvos em `outputs/` e podem ser exportados junto dos resultados. Os arquivos grandes de pesos não são versionados no GitHub.

## 4. Resultados e evidências

A execução de 15/10/2026 está documentada em [evidences/](../evidences/). Essa pasta inclui métricas, JSONs das respostas, históricos de loss, gráficos e [capturas de tela](../evidences/screenshots/).

Para uma nova execução, `python scripts/export_evidence.py` copia os arquivos selecionados de `results/` e `outputs/` para `evidences/`. O relatório pode ser gerado com `python scripts/build_markdown_report.py`.
