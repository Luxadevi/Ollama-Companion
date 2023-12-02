import gradio as gr
import os
import subprocess
import threading

def run_command(model_folder, out_type):
    base_dir = "llama.cpp/models"
    target_dir = f"{base_dir}/{model_folder}/High-Precision-Quantization"
    output_file = f"{model_folder}-{out_type}.gguf"

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Construct the command as a list
    command = [
        "python", "llama.cpp/convert.py", os.path.join(base_dir, model_folder),
        "--outfile", os.path.join(target_dir, output_file),
        "--outtype", out_type
    ]

    try:
        subprocess.run(command, check=True)
        return "Command completed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error in command execution: {e}"


def create_high_ui():
    # Path to the directory
    models_dir = "llama.cpp/models/"

    # Check if the directory exists and list folders
    if os.path.exists(models_dir):
        model_folders = [f for f in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, f))]
    else:
        model_folders = ["Directory not found"]

    def trigger_command(model_folder, out_type):
        # Run the command and return the status
        return run_command(model_folder, out_type)

    with gr.Blocks() as high_ui:
        gr.Markdown("### High Level Interface")
        with gr.Row():
            model_folder_input = gr.Dropdown(label="Select a Model Folder", choices=model_folders)
            out_type_input = gr.Radio(label="Select Output Type", choices=["Q8_0", "f16", "f32"], value="Q8_0")
            run_button = gr.Button("Run Command")
        status_output = gr.Textbox(label="Status")
        run_button.click(trigger_command, inputs=[model_folder_input, out_type_input], outputs=[status_output])

    return high_ui
