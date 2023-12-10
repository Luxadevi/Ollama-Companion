import gradio as gr

def create_model_push_interface():
    with gr.Blocks() as block:
        with gr.Tab("Model Push"):
            gr.Textbox(value="Hello World", label="Your Text")

    return block
