import os
import subprocess
import threading
import queue
import streamlit as st
from shared import shared

# Initialize queue and start a background thread for processing commands
command_queue = queue.Queue()

def process_queue():
    while True:
        model_folder, out_type, use_docker = command_queue.get()
        result = run_command(model_folder, out_type, use_docker)
        print(result)
        command_queue.task_done()

def run_command(model_folder, out_type, use_docker):
    base_dir = "llama.cpp/models"
    input_dir = f"{base_dir}/{model_folder}"
    target_dir = f"{input_dir}/High-Precision-Quantization"
    output_file = f"{model_folder}-{out_type}.GGUF"

    os.makedirs(target_dir, exist_ok=True)

    if use_docker:
        docker_image = "luxaplexx/convert-compaan-ollama"
        command = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(base_dir)}:/models",
            docker_image, "convert", f"/models/{model_folder}",
            "--outfile", f"/models/{model_folder}/High-Precision-Quantization/{output_file}",
            "--outtype", out_type.lower()
        ]
    else:
        command = [
            "python3", "llama.cpp/convert.py", input_dir,
            "--outfile", f"{target_dir}/{output_file}",
            "--outtype", out_type.lower()  # Convert out_type to lowercase
        ]

    try:
        subprocess.run(command, check=True)
        return "Command completed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error in command execution: {e}"


def trigger_command(model_folder, options, use_docker):
    for option in options:
        if options[option]:
            command_queue.put((model_folder, option.lower(), use_docker))
    return "Commands queued. They will run sequentially."

def show_high_precision_quantization_page():
    st.title("High Precision Quantization")

    models_dir = "llama.cpp/models/"
    model_folders = [f for f in os.listdir(models_dir) if os.path.isdir(os.path.join(models_dir, f))] if os.path.exists(models_dir) else ["Directory not found"]

    model_folder = st.selectbox("Select a Model Folder", model_folders)

    options = {option: st.checkbox(label=option) for option in shared['checkbox_high_options']}

    use_docker = st.checkbox("Use Docker Container")

    if st.button("Run Commands"):
        status = trigger_command(model_folder, options, use_docker)
        st.text(status)

threading.Thread(target=process_queue, daemon=True).start()
