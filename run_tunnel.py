import subprocess
import re
import threading
import time

def start_tunnel():
    print("Starting Cloudflare Tunnel...")
    # Start the Cloudflare Tunnel and capture its output
    process = subprocess.Popen(['pycloudflared', 'tunnel', '--url', 'http://127.0.0.1:8501'],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Read the output line by line and search for the URL for 10 seconds
    start_time = time.time()
    while time.time() - start_time < 10:  # Run for 10 seconds
        line = process.stdout.readline()
        if '.trycloudflare.com' in line:
            url = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if url:
                print(f"Tunnel URL: {url.group()}")
                break

    # After 10 seconds, continue running without printing
    while True:
        process.stdout.readline()
        if process.poll() is not None:
            break  # Exit the loop if the process ends

def main():
    try:
        # Start the tunnel in a separate thread
        tunnel_thread = threading.Thread(target=start_tunnel)
        tunnel_thread.start()

        # You can perform other tasks here or just wait for the thread
        tunnel_thread.join()  # Optionally, wait indefinitely for the thread
    except Exception as e:
        print(f"Error starting tunnel: {e}")

if __name__ == "__main__":
    main()
