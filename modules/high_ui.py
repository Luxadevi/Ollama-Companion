import gradio as gr
import os

def create_high_ui():
    # Path to the directory
    models_dir = "llama.cpp/models/"

    # Check if the directory exists
    if os.path.exists(models_dir):
        # List only folders in the directory
        model_folders = [f for f in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, f))]
    else:
        model_folders = ["Directory not found"]

    with gr.Blocks() as high_ui:
        gr.Markdown("### High Level Interface")

        # Dropdown menu populated with folders from the directory
        gr.Dropdown(label="Select a Model Folder", choices=model_folders)

        # Radio buttons for selection
        gr.Radio(label="Select Mode", choices=["Q8_0", "fp16", "fp32"], value="Q8_0")
        # Add more components for High UI here

    return high_ui
