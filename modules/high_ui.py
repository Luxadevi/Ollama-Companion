import gradio as gr
import os
import subprocess
import queue
import threading

from apscheduler.schedulers.background import BackgroundScheduler

# Initialize APScheduler
scheduler = BackgroundScheduler()
scheduler.start()
command_queue = queue.Queue()

def process_queue():
    while True:
        model_folder, out_type = command_queue.get()
        result = run_command(model_folder, out_type)
        print(result)  # Or handle the result in some other way
        command_queue.task_done()

def run_command(model_folder, out_type):
    base_dir = "llama.cpp/models"
    target_dir = f"{base_dir}/{model_folder}/High-Precision-Quantization"
    output_file = f"{model_folder}-{out_type}.gguf"

    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Construct the command as a list
    command = [
        "python3", "llama.cpp/convert.py", os.path.join(base_dir, model_folder),
        "--outfile", os.path.join(target_dir, output_file),
        "--outtype", out_type
    ]

    try:
        subprocess.run(command, check=True)
        return "Command completed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error in command execution: {e}"
def trigger_command(model_folder, q8_0, f16, f32):
    if q8_0:
        command_queue.put((model_folder, "q8_0"))
    if f16:
        command_queue.put((model_folder, "f16"))
    if f32:
        command_queue.put((model_folder, "f32"))
    return "Commands queued. They will run sequentially."

def create_high_ui():
    # Path to the directory
    models_dir = "llama.cpp/models/"

    if os.path.exists(models_dir):
        model_folders = [f for f in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, f))]
    else:
        model_folders = ["Directory not found"]

    with gr.Blocks() as high_ui:
        gr.Markdown("### High Precision Quantization")
        with gr.Row():
            model_folder_input = gr.Dropdown(label="Select a Model Folder", choices=model_folders)
            q8_0_input = gr.Checkbox(label="Q8_0")
            f16_input = gr.Checkbox(label="F16")
            f32_input = gr.Checkbox(label="F32")
            run_button = gr.Button("Run Commands")
        status_output = gr.Textbox(label="Status")
        run_button.click(trigger_command, inputs=[model_folder_input, q8_0_input, f16_input, f32_input], outputs=[status_output])

    return high_ui

# Start the queue processing thread
threading.Thread(target=process_queue, daemon=True).start()


