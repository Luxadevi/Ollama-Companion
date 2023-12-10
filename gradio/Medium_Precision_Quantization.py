import os
import subprocess
import streamlit as st
from shared import shared  # Importing the shared dictionary
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

def list_gguf_files(models_dir):
    gguf_files = []
    if os.path.exists(models_dir):
        for model_folder in os.listdir(models_dir):
            hpq_folder = os.path.join(models_dir, model_folder, 'High-Precision-Quantization')
            if os.path.exists(hpq_folder) and os.path.isdir(hpq_folder):
                for file in os.listdir(hpq_folder):
                    if file.endswith('.gguf'):
                        gguf_files.append(os.path.join(model_folder, 'High-Precision-Quantization', file))
    return gguf_files

def schedule_quantize_task(command):
    try:
        subprocess.run(command, check=True)
        return f"Task completed: {' '.join(command)}"
    except subprocess.CalledProcessError as e:
        return f"Error in task execution: {e}"

def trigger_command(modelpath, options, use_docker):
    debug_output = ""
    base_command = "./llama.cpp/quantize"
    model_name_only, _, model_file = modelpath.partition('/High-Precision-Quantization/')

    medium_precision_dir = f"./llama.cpp/models/{model_name_only}/Medium-Precision-Quantization"
    os.makedirs(medium_precision_dir, exist_ok=True)

    for option in options:
        if options[option]:
            source_path = f"./llama.cpp/models/{model_name_only}/High-Precision-Quantization/{model_file}"
            modified_model_file = model_file.replace('f16.gguf', '').replace('q8_0.gguf', '').replace('f32.gguf', '')
            output_path = f"{medium_precision_dir}/{modified_model_file}-{option.upper()}.GGUF"

            if use_docker:
                docker_image = "luxaplexx/convert-compaan-ollama"
                command = [
                    "docker", "run", "--rm",
                    "-v", f"{os.path.abspath('./llama.cpp/models')}:/models",
                    docker_image, "quantize", f"/models/{model_name_only}/High-Precision-Quantization/{model_file}",
                    f"/models/{model_name_only}/Medium-Precision-Quantization/{modified_model_file}-{option.upper()}.GGUF", option
                ]
            else:
                command = [base_command, source_path, output_path, option]

            # Schedule the task
            scheduler.add_job(schedule_quantize_task, args=[command])
            debug_command_str = ' '.join(command)
            debug_output += f"Scheduled: {debug_command_str}\n"

    if not debug_output:
        debug_output = "No options selected."

    return debug_output

def show_medium_precision_quantization_page():
    st.title("Medium Precision Quantization")

    models_dir = "llama.cpp/models/"
    gguf_files = list_gguf_files(models_dir)

    selected_gguf_file = st.selectbox("Select a GGUF File", gguf_files)
    options = {option: st.checkbox(label=option) for option in shared['checkbox_options']}
    use_docker = st.checkbox("Use Docker Container")

    if st.button("Run Selected Commands"):
        status = trigger_command(selected_gguf_file, options, use_docker)
        st.text_area("Debug Output", status, height=300)



# Show the Streamlit page
show_medium_precision_quantization_page()
