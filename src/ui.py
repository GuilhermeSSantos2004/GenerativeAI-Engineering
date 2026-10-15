"""Interface Gradio para inserir prompts e comparar modelo base/LoRA."""
import argparse
from functools import lru_cache
from pathlib import Path

import gradio as gr
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.common import MODEL_ID, generate_answer


@lru_cache(maxsize=2)
def load_model(variant, adapter_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID, torch_dtype=dtype
    ).to(device)
    if variant == "Treinado (LoRA)":
        if not adapter_path or not Path(adapter_path).exists():
            raise FileNotFoundError("Adapter LoRA ainda não foi treinado: " + adapter_path)
        model = PeftModel.from_pretrained(model, adapter_path, is_trainable=False)
    model.eval()
    return model, tokenizer


def make_app(adapter_path):
    has_adapter = bool(adapter_path and Path(adapter_path).exists())
    available = ["Original (baseline)"] + (["Treinado (LoRA)"] if has_adapter else [])
    with gr.Blocks(title="Python Debug LLM - CP2/CP3") as demo:
        gr.Markdown(
            "# Python Debug LLM · CP2/CP3\n"
            "Assistente especializado em identificar e corrigir erros de Python. "
            "O modelo é executado diretamente no runtime, sem API comercial.\n\n"
            "**Atenção:** as respostas podem conter erros. Execute o código sugerido "
            "em ambiente de testes antes de utilizá-lo."
        )
        with gr.Row():
            variant = gr.Dropdown(
                choices=available, value=available[-1],
                label="Modelo para comparação"
            )
            temperature = gr.Slider(
                minimum=0, maximum=1, value=0.2, step=0.1,
                label="Temperatura"
            )
            max_tokens = gr.Slider(
                minimum=64, maximum=320, value=180, step=16,
                label="Máximo de tokens"
            )
        chatbot = gr.Chatbot(label="Conversa", type="messages", height=430)
        message = gr.Textbox(
            label="Seu prompt",
            lines=5,
            placeholder='Cole um erro Python, por exemplo: print(valor)\nNameError: name \'valor\' is not defined'
        )
        with gr.Row():
            send = gr.Button("Enviar", variant="primary")
            clear = gr.Button("Limpar conversa")

        def reply(user_text, history, chosen, temp, tokens):
            history = history or []
            if not user_text.strip():
                return history, ""
            model, tokenizer = load_model(chosen, adapter_path)
            answer = generate_answer(
                model, tokenizer, user_text,
                max_new_tokens=int(tokens), temperature=float(temp)
            )
            return history + [
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": answer},
            ], ""

        params = [message, chatbot, variant, temperature, max_tokens]
        send.click(reply, inputs=params, outputs=[chatbot, message])
        message.submit(reply, inputs=params, outputs=[chatbot, message])
        clear.click(lambda: ([], ""), outputs=[chatbot, message])
        gr.Markdown(
            f"**Runtime:** {'GPU CUDA' if torch.cuda.is_available() else 'CPU'} · "
            f"**Modelo base:** {MODEL_ID} · "
            f"**Adapter encontrado:** {'sim' if has_adapter else 'não'}"
        )
    return demo


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--adapter", default="outputs/experiment_a/final_adapter")
    p.add_argument("--share", action="store_true",
                   help="Cria URL pública temporária; use somente para dados não sensíveis")
    p.add_argument("--port", type=int, default=7860)
    args = p.parse_args()
    app = make_app(args.adapter)
    app.queue().launch(server_name="0.0.0.0", server_port=args.port, share=args.share)


if __name__ == "__main__":
    main()
