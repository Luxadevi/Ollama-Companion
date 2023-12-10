import os
import subprocess
import threading
import streamlit as st
import requests
import yaml
from shared import shared  # Importing the shared dictionary
from apscheduler.schedulers.background import BackgroundScheduler
import socket
import time

## Way to big is litellm running workflow
def is_process_running(process_name):
    """Check if there is any running process that contains the given name."""
    try:
        process = subprocess.run(["pgrep", "-f", process_name], capture_output=True, text=True)
        return process.stdout != ""
    except subprocess.CalledProcessError:
        return False

def kill_process(process_name):
    """Kill the process with the given name."""
    try:
        subprocess.run(["pkill", "-f", process_name])
    except Exception as e:
        print(f"Error killing process {process_name}: {e}")

def is_port_in_use(port):
    """Check if the given port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Kill process running on the given port."""
    try:
        subprocess.run(["fuser", "-k", f"{port}/tcp"])
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")

def start_litellm_proxy():
    litellm_process_name = "litellm"
    litellm_port = 8000

    # Terminate existing LiteLLM processes and free up port 8000 if necessary
    if is_process_running(litellm_process_name):
        print("LiteLLM is already running. Terminating existing process.")
        kill_process(litellm_process_name)

    if is_port_in_use(litellm_port):
        print(f"Port {litellm_port} is in use. Terminating process on this port.")
        kill_process_on_port(litellm_port)

    # Define paths for log and config
    log_dir = os.path.join('.', 'logs')
    config_dir = os.path.join('.', 'configs')
    log_file_path = os.path.join(log_dir, 'litellmlog')
    config_file_path = os.path.join(config_dir, 'config.yaml')

    # Start the LiteLLM proxy
    litellm_proxycmd = f"litellm --config {config_file_path} --debug --add_function_to_prompt >> {log_file_path} 2>&1 &"
    subprocess.Popen(litellm_proxycmd, shell=True)


def read_litellm_log():
    log_dir = os.path.join(os.path.dirname(__file__), '.', 'logs')
    log_file_path = os.path.join(log_dir, 'litellmlog')

    try:
        # Wait for some time for the proxy to start and log
        time.sleep(15)

        # Read the log file and return the relevant lines
        with open(log_file_path, "r") as log_file:
            lines = log_file.readlines()

        for line in lines:
            if "LiteLLM: Proxy initialized with Config, Set models:" in line:
                model_lines = [line.strip() for line in lines[lines.index(line) + 1:] if line.strip()]
                return "\n".join([line.strip()] + model_lines)

        return "Relevant log information not found."
    except Exception as e:
        return f"Error: {str(e)}"


##Polling logic. Uses aspscheduler to check every 15 seconds if there is an update to
##The ollama api and when there are updates add it to the config.yaml

scheduler = BackgroundScheduler()

def poll_api():
    api_url = shared['api_endpoint']['url']
    response = requests.get(f"{api_url}/api/tags")
    if response.status_code == 200:
        json_data = response.json()
        model_names = [model['name'] for model in json_data.get('models', [])]
        update_config_file(model_names)

def start_polling():
    # Add the polling task to the scheduler
    scheduler.add_job(poll_api, 'interval', seconds=15)
    scheduler.start()
    return "Polling started"

def stop_polling():
    # Shutdown the scheduler
    scheduler.shutdown()
    return "Polling stopped"

## Updating the config.yaml when changes passed

def update_config_file(model_names):
# Adjust the path to the config directory
    config_dir = os.path.join(os.path.dirname(__file__), 'configs')
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

    if 'model_list' not in config:
        config['model_list'] = []

    existing_models = set(model['model_name'] for model in config['model_list'])
    needs_update = False

    # Update the 'model_list' with new models
    for model_name in model_names:
        full_model_name = f"ollama/{model_name}"
        if full_model_name not in existing_models:
            entry = {
                'model_name': full_model_name,
                'litellm_params': {
                    'model': full_model_name,
                    'api_base': shared['api_endpoint']['url'],
                    'json': True,
                    'drop_params': True
                }
            }
            config['model_list'].append(entry)
            existing_models.add(full_model_name)
            needs_update = True

    # Write the updated configuration back to the file
    if needs_update:
        with open(config_file_path, "w") as file:
            yaml.dump(config, file, default_flow_style=False)
        print("Config file updated successfully.")

### Interface creator

def show_litellm_proxy_page():
    st.title('LiteLLM Proxy')

    if st.button('Start LiteLLM Proxy'):
        # Start LiteLLM proxy in a separate thread
        threading.Thread(target=start_litellm_proxy, daemon=True).start()
        st.success("LiteLLM Proxy started")

    if st.button('Read LiteLLM Log'):
        log_output = read_litellm_log()
        st.text_area("Log Output", log_output, height=300)

            # Add buttons for starting and stopping polling
    if st.button('Start Polling'):
        message = start_polling()
        st.success(message)

    if st.button('Stop Polling'):
        message = stop_polling()
        st.success(message)
    if st.button('Kill Existing LiteLLM Processes'):
            litellm_process_name = "litellm"
            if is_process_running(litellm_process_name):
                kill_process(litellm_process_name)
                st.success(f"Killed existing {litellm_process_name} processes")
            else:
                st.info("No LiteLLM processes found")

    # Button to free up port 8000 if it's in use
    if st.button('Free Up Port 8000'):
        litellm_port = 8000
        if is_port_in_use(litellm_port):
            kill_process_on_port(litellm_port)
            st.success(f"Freed up port {litellm_port}")
        else:
            st.info(f"Port {litellm_port} is not in use")

