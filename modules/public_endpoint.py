import gradio as gr
import threading
import os
import time


# Get the directory of the current module
module_dir = os.path.dirname(__file__)

# Define the log directory and log file paths
log_dir = os.path.join(module_dir, '..', 'logs')  # Adjust the path as necessary
endpoint_log_path = os.path.join(log_dir, 'endpoint.log')

# Define the tools directory path
tools_dir = os.path.join(module_dir, '..', 'tools')  # Adjust the path as necessary

def flask_endpoint():
    # Set the path to your Flask endpoint script
    endpoint_path = os.path.join(tools_dir, 'endpoint.py')
    os.system(f"PYTHONUNBUFFERED=1 python3 {endpoint_path} > {endpoint_log_path} 2>&1")

def start_endpoint_and_get_last_2_lines():
    global flask_thread
    try:
        # Start the Flask endpoint in a new thread
        flask_thread = threading.Thread(target=flask_endpoint)
        flask_thread.start()

        # Wait for a reasonable amount of time for the server to start (adjust as needed)
        time.sleep(15)

        # Read the last 2 lines from the endpoint.log file
        with open(endpoint_log_path, "r") as log_file:
            lines = log_file.readlines()
            last_2_lines = "".join(lines[-2:])  # Concatenate the last 2 lines

        result = f"OpenAI is available at /openai\n{last_2_lines}"
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def kill_endpoint():
    global flask_thread
    try:
        # Attempt to stop the Flask thread
        if flask_thread and flask_thread.is_alive():
            flask_thread.join(1)  # You may adjust the timeout
            flask_thread = None
        return "Endpoint killed successfully."
    except Exception as e:
        return f"Error: {str(e)}"

def create_public_endpoint_interface():
    with gr.Blocks() as block:
        with gr.Tab("Public Endpoint"):
            start_endpoint_button = gr.Button("Start Public Endpoint")
            last_2_lines_output = gr.Textbox(label="Endpoint information", interactive=False)
            kill_endpoint_button = gr.Button("Kill Endpoint")

            start_endpoint_button.click(start_endpoint_and_get_last_2_lines, inputs=[], outputs=[last_2_lines_output])
            kill_endpoint_button.click(kill_endpoint, inputs=[], outputs=[last_2_lines_output])

    return block
