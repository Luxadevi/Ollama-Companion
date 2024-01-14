import subprocess
import threading
import re

def launch_start_script():
    script_path = '/content/Ollama-Companion/start.sh'
    try:
        subprocess.run([script_path], check=True, cwd='/content/Ollama-Companion', shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    else:
        print(f"Script {script_path} has been successfully launched.")

def run_ollama():
    print("Starting Ollama...")
    subprocess.Popen(['python3', '/content/ollama.py'])

def main():
    ollama_thread = threading.Thread(target=run_ollama)
    ollama_thread.start()

    # Now the main thread can continue doing other things.
    # Note: Since we are not waiting for ollama_thread to finish, 
    # we won't use ollama_thread.join() here.

    launch_start_script()

if __name__ == "__main__":
    main()
