import os
import threading
import time
import subprocess
import streamlit as st

# Get the directory of the current module
module_dir = os.path.dirname(__file__)

# Define the log directory and log file paths
log_dir = os.path.join(module_dir, 'logs')
endpoint_log_path = os.path.join(log_dir, 'endpoint.log')

# Define the tools directory path
tools_dir = os.path.join(module_dir, 'tools')

flask_thread = None

def flask_endpoint():
    # Set the path to your Flask endpoint script
    endpoint_path = os.path.join(tools_dir, 'endpoint.py')
    os.system(f"PYTHONUNBUFFERED=1 python3 {endpoint_path} > {endpoint_log_path} 2>&1")

def start_endpoint_and_get_last_2_lines():
    global flask_thread
    try:
        flask_thread = threading.Thread(target=flask_endpoint, daemon=True)
        flask_thread.start()

        time.sleep(15)

        with open(endpoint_log_path, "r") as log_file:
            lines = log_file.readlines()
            last_2_lines = "".join(lines[-2:])

        result = f"OpenAI is available at /openai\n{last_2_lines}"
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def kill_endpoint():
    try:
        # Find processes using port 5000 and kill them
        pids = subprocess.check_output(["lsof", "-t", "-i:5000"]).decode().splitlines()
        for pid in pids:
            subprocess.run(["kill", "-9", pid])

        return "Endpoint killed successfully."
    except Exception as e:
        return f"Error: {str(e)}"
    


def show_public_endpoint_page():
    st.title("Public Endpoint Management")

    if st.button("Start Endpoint"):
        result = start_endpoint_and_get_last_2_lines()
        
        # Check if result contains URLs and convert them to Markdown links
        if "Running on" in result:
            lines = result.split('\n')
            for i, line in enumerate(lines):
                if line.startswith("* Running on"):
                    url = line.split()[3]
                    lines[i] = f"* Running on [link]({url})"
                elif line.startswith("* Traffic stats available on"):
                    url = line.split()[4]
                    lines[i] = f"* Traffic stats available on [link]({url})"
            result = '\n'.join(lines)
        
        # Display the result as Markdown
        st.markdown(result)

    if st.button("Kill Endpoint"):
        result = kill_endpoint()
        st.text(result)
