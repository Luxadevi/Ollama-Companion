import subprocess
import re
import os

def start_tunnel():
    print("Starting Cloudflare Tunnel...")
    # Start the Cloudflare Tunnel and capture its output
    process = subprocess.Popen(['pycloudflared', 'tunnel', '--url', 'http://127.0.0.1:8501'],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Read the output line by line and search for the URL
    for line in iter(process.stdout.readline, ''):
        if '.trycloudflare.com' in line:
            url = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if url:
                print(f"Tunnel URL: {url.group()}")
                break

def run_streamlit(streamlit_script_path):
    print("Starting Streamlit App...")
    subprocess.call(['streamlit', 'run', streamlit_script_path])

def main():
    streamlit_script_path = '/content/Ollama-Companion/main.py'

    # Check if the specific Streamlit script exists in the Jupyter environment
    if os.path.exists(streamlit_script_path):
        print("Running Streamlit in Jupyter environment...")
        run_streamlit(streamlit_script_path)
    else:
        print("Running Streamlit in a non-Jupyter environment...")
        start_tunnel()
        run_streamlit('main.py')

if __name__ == "__main__":
    main()
