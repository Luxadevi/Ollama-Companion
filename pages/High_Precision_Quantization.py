from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import threading
from pathlib import Path
import streamlit as st
from modules.shared import shared
import sys
import queue

# Initialize queue
command_queue = queue.Queue()

# Existing function definitions (find_llama_models_dir, run_command, trigger_command)

def process_queue():
    if not command_queue.empty():
        model_folder, out_type, use_docker = command_queue.get()
        result = run_command(model_folder, out_type, use_docker)
        print(result)
        command_queue.task_done()

# Set up APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(process_queue, 'interval', seconds=10)  # Adjust the interval as needed
scheduler.start()

# Initialize queue and start a background thread for processing commands

@st.cache_data
def find_llama_models_dir(start_path, max_up=4, max_down=3):
    def search_upwards(path, depth):
        if depth > max_up:
            return None
        if (path / "llama.cpp/models").exists():
            return path / "llama.cpp/models"
        return search_upwards(path.parent, depth + 1)
    
    @st.cache_data
    def search_downwards(path, depth):
        if depth > max_down:
            return None
        if (path / "llama.cpp/models").exists():
            return path / "llama.cpp/models"
        for child in [d for d in path.iterdir() if d.is_dir()]:
            found = search_downwards(child, depth + 1)
            if found:
                return found
        return None

    # Search upwards
    found_path = search_upwards(start_path, 4)
    if found_path:
        return found_path  # Return the found 'llama.cpp/models' directory

    # Search downwards
    return search_downwards(start_path, 3)


# Use the function to find the base directory
# current_path = Path(__file__).resolve()
# base_dir = find_llama_models_dir(current_path)

# if not base_dir:
#     print("Error: llama.cpp/models/ directory not found.")
# else:
#     print("llama.cpp/models/ found at:", base_dir)




def run_command(model_folder, out_type, use_docker):
    base_dir = Path("llama.cpp/models")
    input_dir = base_dir / model_folder
    target_dir = input_dir / "High-Precision-Quantization"
    output_file = f"{model_folder}-{out_type}.GGUF"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Correct path for convert.py
    convert_script_path = base_dir.parent / "convert.py"  # Assuming convert.py i

    if use_docker:
        docker_image = "luxaplexx/convert-compaan-ollama"
        # Docker volume paths need to be in Linux format even on Windows
        if sys.platform.startswith('win'):
            volume_path = base_dir.resolve().drive  # This will be 'D:' on Windows if base_dir is on D drive
        else:
            volume_path = base_dir.resolve().as_posix()  # On Unix-like systems, the full path is used
        output_path = Path(f"./models/{model_folder}/High-Precision-Quantization/{output_file}").as_posix()
   
            
        command = [
            "docker", "run", "--rm",
            "-v", f"{volume_path}/models",
            docker_image, "convert", Path("./models") / model_folder,
            "--outfile", output_path.as_posix(),
            "--outtype", out_type.lower()
        ]
        print("ran with docker", command)
    else:
        command = [
            "python3", str(convert_script_path),
            str(input_dir),
            "--outfile", str(target_dir / output_file),
            "--outtype", out_type.lower()
        ]
    print("First statement", target_dir)
    try:
        subprocess.run(command, check=True)
        return "Command completed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error in command execution: {e}"


def trigger_command(model_folder, options, use_docker):
    if not any(options.values()):
        return "Error: No quantization type selected."
    for option in options:
        if options[option]:
            command_queue.put((model_folder, option.lower(), use_docker))
    return "Commands queued. They will run sequentially."



# Old UI code
# def show_high_precision_quantization_page():

st.title("High Precision Quantization")

models_dir = Path("llama.cpp/models/")
model_folders = [f.name for f in models_dir.iterdir() if f.is_dir()] if models_dir.exists() else ["Directory not found"]

model_folder = st.selectbox("Select a Model Folder", model_folders)
options = {option: st.checkbox(label=option) for option in shared['checkbox_high_options']}
use_docker = st.checkbox("Use Docker Container")

if st.button("Run Commands"):
    if not any(options.values()):
        st.error("Please select at least one quantization type before running commands.")
    elif use_docker and not any(options.values()):
        st.error("Please select at least one quantization type along with the Docker option.")
    else:
        status = trigger_command(model_folder, options, use_docker)
        st.text(status)


with st.expander("Step One: Model Conversion with High Precision", expanded=False):
    st.markdown("""
    **Step One: Model Conversion with High Precision**


    **Conversion Process:**

    1. **Select a Model Folder:** Choose a folder containing the model you wish to convert, found within `llama.cpp/models`.
    2. **Set Conversion Options:** Select the desired conversion options from the provided checkboxes (e.g., Q, Kquants).
    3. **Docker Container Option:** Opt to use a Docker container for added flexibility and compatibility.
    4. **Execute Conversion:** Click the "Run Commands" button to start the conversion process.
    5. **Output Location:** Converted models will be saved in the `High-Precision-Quantization` subfolder within the chosen model folder.

    Utilize this process to efficiently convert models while maintaining high precision and compatibility with `llama.cpp`.
    """)
# Start the thread to process commands
threading.Thread(target=process_queue, daemon=True).start()
