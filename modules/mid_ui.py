import gradio as gr
import os
from .shared import shared  # Import the shared dictionary
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler


# native quanting command and pathing
def trigger_command(modelpath, *checkbox_options):
    debug_output = ""
    base_command = "./llama.cpp/quantize"
    model_name_only, _, model_file = modelpath.partition('/High-Precision-Quantization/')

    for option, checked in zip(shared['checkbox_options'], checkbox_options):
        if checked:
            source_path = f"./llama.cpp/models/{model_name_only}/High-Precision-Quantization/{model_file}"
            modified_model_file = model_file.replace('f16.gguf', '').replace('q8_0.gguf', '').replace('f32.gguf', '')
            output_path = f"./llama.cpp/models/{model_name_only}/Medium-Precision-Quantization/{modified_model_file}-{option.upper()}.gguf"
            command = [base_command, source_path, output_path, option]

            # Schedule the command for execution
            scheduler.add_job(execute_command, args=[command])

            # Add to debug output
            debug_command_str = ' '.join(command)
            debug_output += f"Scheduled: {debug_command_str}\n"

    if not debug_output:
        debug_output = "No options selected."
    
    return debug_output


# Initialize APScheduler
scheduler = BackgroundScheduler()
scheduler.start()

## Runcommand by scheduler
def execute_command(command):
    try:
        subprocess.run(command, check=True)
        return f"Command {' '.join(command)} completed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error in command execution: {e}"




### Create ui to be called from quant_ui.py
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
        gr.Markdown("### Medium Precision Quantization")
        with gr.Row():
            dropdown = gr.Dropdown(label="Select a GGUF File", choices=gguf_files, value=gguf_files[0] if gguf_files else "")
            checkboxes = [gr.Checkbox(label=option) for option in shared['checkbox_options']]
        
        run_button = gr.Button("Run Selected Commands")
        debug_output = gr.TextArea(label="Debug Output")
        run_button.click(trigger_command, inputs=[dropdown, *checkboxes], outputs=debug_output)

    return mid_ui
