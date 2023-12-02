import gradio as gr
import os
from .shared import shared  # Import the shared dictionary

def create_mid_ui():
    models_dir = "llama.cpp/models/"
    gguf_files = []

    # Check if the models directory exists and list .gguf files
    if os.path.exists(models_dir):
        for model_folder in os.listdir(models_dir):
            hpq_folder = os.path.join(models_dir, model_folder, 'High-Precision-Quantization')
            if os.path.exists(hpq_folder) and os.path.isdir(hpq_folder):
                for file in os.listdir(hpq_folder):
                    if file.endswith('.gguf'):
                        gguf_files.append(os.path.join(model_folder, 'High-Precision-Quantization', file))
    else:
        gguf_files = ["Models directory not found"]

    with gr.Blocks() as mid_ui:  # Corrected indentation
        gr.Markdown("### Mid Precision Quantization")
        with gr.Row():
            dropdown = gr.Dropdown(label="Select a GGUF File", choices=gguf_files)
        with gr.Row():
            checkboxes = [gr.Checkbox(label=option) for option in shared['checkbox_options']]
        
        # Example of a button to handle the selections (implement your own logic)
        run_button = gr.Button("Run Selected Commands")
        status_output = gr.Textbox(label="Status")
        # Placeholder function for button click
        run_button.click(lambda *args: "Commands queued", inputs=checkboxes, outputs=status_output)

    return mid_ui
