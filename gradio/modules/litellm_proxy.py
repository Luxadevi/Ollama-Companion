# litellm_proxy.py
import os
import subprocess
import time
import requests
import threading
import yaml
import gradio as gr
from .shared import shared

# Other imports as necessary

polling_active = False
current_model_list = []

# Define the paths to the log and config directories
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
config_dir = os.path.join(os.path.dirname(__file__), '..', 'configs')

# Paths to specific files
log_file_path = os.path.join(log_dir, 'litellmlog')
config_file_path = os.path.join(config_dir, 'config.yaml')

# LiteLLM startup command
litellm_proxycmd = f"PYTHONUNBUFFERED=1 litellm --config {config_file_path} --debug --add_function_to_prompt >> {log_file_path} 2>&1 &"

def start_litellm_proxy_and_read_log():
    try:
        

        # Start the LiteLLM proxy using subprocess with the updated command
        subprocess.Popen(litellm_proxycmd, shell=True)

        # Wait for some time for the proxy to start and log
        time.sleep(15)

        # Read the log file and search for specific lines
        with open(log_file_path, "r") as log_file:
            lines = log_file.readlines()

        # Find and return the relevant lines
        for i, line in enumerate(lines):
            if "LiteLLM: Proxy initialized with Config, Set models:" in line:
                # Assuming the model names are listed in the following lines
                model_lines = [lines[i + j].strip() for j in range(1, len(lines) - i) if lines[i + j].strip()]
                return "\n".join([line.strip()] + model_lines)

        return "Relevant log information not found."
    except Exception as e:
        return f"Error: {str(e)}"

def kill_litellm_proxy():
    try:
        # Command to kill the LiteLLM proxy process
        kill_command = "pkill -f 'litellm --config'"

        # Execute the kill command
        os.system(kill_command)

        return "LiteLLM proxy process terminated."
    except Exception as e:
        return f"Error: {str(e)}"

def poll_api():
    global polling_active
    while polling_active:
        api_url = shared['api_endpoint']['url']
        response = requests.get(f"{api_url}/api/tags")
        if response.status_code == 200:
            json_data = response.json()
            model_names = [model['name'] for model in json_data.get('models', [])]
            update_config_file(model_names)
        time.sleep(15)

def start_polling():
    global polling_active
    polling_active = True
    threading.Thread(target=poll_api).start()
    return "Polling started"

def stop_polling():
    global polling_active
    polling_active = False
    return "Polling stopped"

def is_litellm_running():
    """Check if LiteLLM is currently running."""
    try:
        # Using subprocess to check if litellm process is running
        result = subprocess.run(["pgrep", "-f", "litellm --config"], capture_output=True, text=True)
        return result.stdout != ""
    except Exception as e:
        print(f"Error checking if LiteLLM is running: {e}")
        return False

def restart_litellm():
    """Restart the LiteLLM process."""
    try:
        # Kill the current LiteLLM process
        kill_litellm_proxy()
        # Wait for a moment to ensure the process has been killed
        time.sleep(5)
        # Start the LiteLLM process again
        start_litellm_proxy_and_read_log()
        print("LiteLLM proxy restarted successfully.")
    except Exception as e:
        print(f"Error restarting LiteLLM: {e}")

def update_config_file(model_names):
    global current_model_list
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'configs')
    config_file_path = os.path.join(config_dir, 'config.yaml')

    # Ensure the config file exists
    if not os.path.exists(config_file_path):
        print(f"Config file not found at {config_file_path}")
        return

    # Read the existing content of the config file
    with open(config_file_path, "r") as file:
        try:
            config = yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            print(f"Error reading config file: {e}")
            return

    # Ensure 'model_list' key exists in the configuration
    if 'model_list' not in config:
        config['model_list'] = []

    existing_models = {model['model_name'] for model in config['model_list']}
    needs_update = False

    # Extract litellm_settings from the existing config
    litellm_settings = config.pop('litellm_settings', {})

    # Update the 'model_list' with new models
    for model_name in model_names:
        full_model_name = f"ollama/{model_name}"
        if full_model_name not in existing_models:
            entry = {
                'model_name': full_model_name,
                'litellm_params': {
                    'model': full_model_name,
                    'api_base': shared['api_endpoint']['url'],  # Use API URL from shared dictionary
                    'json': True,
                    'drop_params': True
                }
            }
            config['model_list'].append(entry)
            existing_models.add(full_model_name)
            needs_update = True

    # Append litellm_settings to the end of the new models
    for entry in config['model_list']:
        if 'litellm_params' in entry:
            entry['litellm_params'].update(litellm_settings)

    # Write the updated configuration back to the file
    with open(config_file_path, "w") as file:
        yaml.dump(config, file, default_flow_style=False)

    if needs_update:
        print("Config file updated successfully.")

def create_litellm_proxy_interface():
    with gr.Blocks() as block:
        with gr.Tab("LiteLLM-Proxy"):
            # Textboxes for displaying logs and status
            litellm_log_output = gr.Textbox(label="LiteLLM Log Output", interactive=False, lines=10)
            litellm_kill_status = gr.Textbox(label="LiteLLM Kill Status", interactive=False, lines=1)
            polling_status = gr.Textbox(label="Polling Status", interactive=False, lines=1)

            # Buttons for starting, stopping, and killing the proxy
            with gr.Row():
                start_litellm_button = gr.Button("Start LiteLLM Proxy")
                kill_litellm_button = gr.Button("Kill LiteLLM Proxy")
                start_polling_button = gr.Button("Start Polling")
                stop_polling_button = gr.Button("Stop Polling")

            # Link the buttons to their respective functions
            start_litellm_button.click(
                fn=start_litellm_proxy_and_read_log,
                inputs=[],
                outputs=[litellm_log_output]
            )

            kill_litellm_button.click(
                fn=kill_litellm_proxy,
                inputs=[],
                outputs=[litellm_kill_status]
            )

            start_polling_button.click(
                fn=start_polling,
                inputs=[],
                outputs=[polling_status]
            )

            stop_polling_button.click(
                fn=stop_polling,
                inputs=[],
                outputs=[polling_status]
            )

    return block
