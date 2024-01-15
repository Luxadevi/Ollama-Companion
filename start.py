import subprocess
import threading
import multiprocessing
import sys
import os

def start_tunnel():
    print("Starting tunnel...")
    # Kill existing tunnel processes
    subprocess.run(['pgrep', '-f', '.*tunnel.*127\.0\.0\.1:8501.*'], stdout=subprocess.PIPE)
    subprocess.run(['xargs', '-r', 'kill', '-9'], input=subprocess.PIPE)

    # Start tunnel
    subprocess.run(['python3', 'run_tunnel.py'])

def start_streamlit():
    print("Starting Streamlit...")
    subprocess.run(['streamlit', 'run', 'Homepage.py'])

def main():
    # Change to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Changed working directory to {script_dir}")

    # Determine the function to run based on command-line arguments
    start_tunnel_process = multiprocessing.Process(target=start_tunnel)
    if '-local' in sys.argv or '-lan' in sys.argv:
        start_tunnel_process = None  # No tunnel needed for local run

    # Start tunnel in a separate process if needed
    if start_tunnel_process:
        start_tunnel_process.start()

    # Start streamlit in a separate thread
    streamlit_thread = threading.Thread(target=start_streamlit)
    streamlit_thread.start()

    # Wait for the tunnel process to finish, if it was started
    if start_tunnel_process:
        start_tunnel_process.join()

    # Wait for the Streamlit thread to finish
    streamlit_thread.join()

if __name__ == "__main__":
    main()
