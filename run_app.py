import subprocess
import re

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
               


def run_streamlit():
    print("Starting Streamlit App...")
    try:
        subprocess.check_call(['streamlit', 'run', './Homepage.py'])
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit: {e}")
    except FileNotFoundError:
        print("Streamlit file not found, checking current directory")
        try:
            subprocess.check_call(['streamlit', 'run', './Homepage.py'])
        except subprocess.CalledProcessError as e:
            print(f"Error running Streamlit from current directory: {e}")

def main():
    try:
        start_tunnel()
    except Exception as e:
        print(f"Error starting tunnel: {e}")

    try:
        run_streamlit()
    except Exception as e:
        print(f"Error running Streamlit: {e}")

if __name__ == "__main__":
    main()
