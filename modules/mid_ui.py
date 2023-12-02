import gradio as gr
import os
from .shared import shared  # Import the shared dictionary
import subprocess

def trigger_command(modelname, *checkbox_options):
    debug_output = ""
    base_command = "./llama.cpp/quantize"

    for option, checked in zip(shared['checkbox_options'], checkbox_options):
        if checked:  
            source_path = f"./models/{modelname}/High-Precision-Quantization/{modelname}.gguf"
            output_path = f"./models/{modelname}/Medium-Precision_Quantazation/{modelname}-{option}/gguf"
            command = [base_command, source_path, output_path, option]

            # Construct the command string for debugging
            debug_command_str = ' '.join(command)
            debug_output += f"Executing: {debug_command_str}\n"

            try:
                subprocess.run(command, check=True)
                debug_output += f"Command for {option} completed successfully.\n"
            except subprocess.CalledProcessError as e:
                debug_output += f"Error in command execution for {option}: {e}\n"

    if not debug_output:
        debug_output = "No options selected."
    
    return debug_output


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

    with gr.Blocks() as mid_ui:
        gr.Markdown("### Mid Level Interface")
        with gr.Row():
            dropdown = gr.Dropdown(label="Select a GGUF File", choices=gguf_files, value=gguf_files[0] if gguf_files else "")
            checkboxes = [gr.Checkbox(label=option) for option in shared['checkbox_options']]
        
        run_button = gr.Button("Run Selected Commands")
        debug_output = gr.TextArea(label="Debug Output")
        run_button.click(trigger_command, inputs=[dropdown, *checkboxes], outputs=debug_output)

    return mid_ui
