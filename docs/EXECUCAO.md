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

Colab Free não garante disponibilidade da GPU nem duração da sessão. Se GPU não estiver disponível, não registre testes em CPU como se tivessem sido feitos em GPU. Retome quando o Colab liberar hardware, ou utilize outro ambiente CUDA.

## 2. Evidência solicitada: GPU DENTRO do VS Code

Há duas formas possíveis:

**Opção A (preferida):** instale a extensão oficial [Google Colab para VS Code](https://marketplace.visualstudio.com/items?itemName=Google.colab), abra o notebook `.ipynb` no VS Code, selecione o kernel do Colab e conecte ao runtime GPU. O comportamento pode variar conforme a versão da extensão. Execute a primeira célula e tire um print do **VS Code inteiro**, mostrando código e saída real `GPU:`, `CUDA disponível: True`, dispositivo `cuda:0` e `nvidia-smi`.

**Opção B:** quando a extensão não conectar, execute o notebook no navegador Colab e obtenha a evidência real por lá, mas **registre honestamente** que o print não é do VS Code; isso pode não atender integralmente a exigência do professor.

Nome sugerido: `evidences/screenshots/gpu_vscode.png`. Capture também `treinamento_a.png`, `treinamento_b.png`, `avaliacao.png` e `frontend.png`.

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

O repositório não envia pesos-base (~centenas de MB); o Transformers faz download do modelo público. Os adapters são armazenados localmente em `outputs/` e podem ser recuperados do ZIP. **Não faça commit do ZIP grande ou de arquivos corporativos/sensíveis.**

## 4. Publicar as evidências no GitHub

Após salvar os arquivos em seu PC, copie `evidences/` para o clone local do repositório e rode:

```bash
git add evidences docs
git commit -m "docs: add real GPU training and evaluation evidence"
git push origin main
```

Inclua manualmente as capturas de tela na pasta `evidences/screenshots/`. Os arquivos `outputs/` e `results/` são ignorados pelo Git; use `scripts/export_evidence.py` para copiar o material selecionado a `evidences/`.
