import gradio as gr
import os
from .shared import shared  # Import the shared dictionary

def create_mid_ui():
    models_dir = "llama.cpp/models/"
    gguf_files = []

    # Check if the models directory exists
    if os.path.exists(models_dir):
        # Iterate through each model folder
        for model_folder in os.listdir(models_dir):
            hpq_folder = os.path.join(models_dir, model_folder, 'High-Precision-Quantization')
            # Check for 'High-Precision-Quantization' subfolder and list .gguf files
            if os.path.exists(hpq_folder) and os.path.isdir(hpq_folder):
                for file in os.listdir(hpq_folder):
                    if file.endswith('.gguf'):
                        gguf_files.append(f"{model_folder}/High-Precision-Quantization/{file}")
    else:
        gguf_files = ["Models directory not found"]


    with gr.Blocks() as mid_ui:
        gr.Markdown("### Mid Level Interface")
        gr.Dropdown(label="Select a GGUF File", choices=gguf_files)
        # You can add more UI components here as needed

    return mid_ui
