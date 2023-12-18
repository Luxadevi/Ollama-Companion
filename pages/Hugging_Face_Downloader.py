import os
import subprocess
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from pathlib import Path
import hashlib
import streamlit as st
from functools import partial
import os
from pathlib import Path
import threading
import time


log_file_path = "download_status.log"

# Initialize Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Global variables for download management
download_queue = []
currently_downloading = False
download_results = []

def download_completed():
    global currently_downloading
    currently_downloading = False
    if download_queue:
        start_next_download()


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()



def start_next_download():
    global currently_downloading
    if not currently_downloading and download_queue:
        task = download_queue.pop(0)
        task()
        currently_downloading = True

# Validate the downloaded files
def validate_file_sha256(file_path, expected_sha256):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest() == expected_sha256


def download_file_task(file_url, download_path, filename, sha256_checksum, start_next_download_callback):
    file_path = download_path / filename
    command = [
        "aria2c", file_url,
        "--max-connection-per-server=16", "--split=8", "--min-split-size=1M",
        "--allow-overwrite=true", "-d", str(download_path), "-o", filename
    ]

    def run_download():
        print(f"Starting download: {command}")
        try:
            subprocess.run(command, check=True)
            result = "validated" if calculate_sha256(file_path) == sha256_checksum else "failed"
            print(result)
            with open(log_file_path, "a") as log_file:
                log_file.write(f"{filename}: Download completed and {result}\n")
        except subprocess.CalledProcessError as e:
            with open(log_file_path, "a") as log_file:
                log_file.write(f"{filename}: Error downloading - {str(e)}\n")
        finally:
            download_completed()


    # Start the download in a separate thread
    download_thread = threading.Thread(target=run_download)
    download_thread.start()


# Monitors download and start next download @ 80%
    # # @st.cache_data
    # def monitor_download():
    #     while not file_path.exists() or os.path.getsize(file_path) < file_size * 0.8:
    #         time.sleep(5)  # Check every 5 seconds
    #     start_next_download_callback()

    # # Start the download in a separate thread
    # download_thread = threading.Thread(target=run_download)
    # download_thread.start()

    # # Start the monitor in a separate thread
    # monitor_thread = threading.Thread(target=monitor_download)
    # monitor_thread.start()

# Gets the filesize and start news download when 80%

# def get_remote_file_size(url):
#     try:
#         response = requests.head(url)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         return int(response.headers.get('Content-Length', 0))
#     except requests.RequestException as e:
#         print(f"Error obtaining file size for {url}: {e}")
#         return 0

# def queue_download(file_links_dict, model_name):
#     current_dir = Path(__file__).resolve().parent
#     download_path = current_dir.parent / f"llama.cpp/models/{model_name.split('/')[-1]}"
#     download_path.mkdir(parents=True, exist_ok=True)

#     for file_name, file_info in file_links_dict.items():
#         file_url, sha256_checksum = file_info['url'], file_info['sha256']
#         # file_size = get_remote_file_size(file_url)  # Get the file size in bytes
#         # download_task = partial(download_file_task, file_url, download_path, file_name, sha256_checksum, file_size, start_next_download)
#         # download_queue.append(download_task)

#     start_next_download()
#     return "Download tasks have been queued."
    



def download_file_task(file_url, download_path, filename, sha256_checksum, file_size, start_next_download_callback):
    file_path = download_path / filename
    command = [
        "aria2c", file_url,
        "--max-connection-per-server=16", "--split=8", "--min-split-size=1M",
        "--allow-overwrite=true", "-d", str(download_path), "-o", filename
    ]

    def run_download():
        print(command)
        try:
            # Run the download command
            subprocess.run(command, check=True)

            # Check if download is valid after completion
            if calculate_sha256(file_path) == sha256_checksum:
                st.write(f"Download completed and validated: {filename}")
            else:
                st.write(f"Checksum validation failed for {filename}")
        except subprocess.CalledProcessError as e:
            st.write(f"Error downloading {filename}: {str(e)}")
        finally:
            download_completed()
# Monitors download and start next download @ 80%
    def monitor_download():
        while not file_path.exists() or os.path.getsize(file_path) < file_size * 0.8:
            time.sleep(5)  # Check every 5 seconds
        start_next_download_callback()

    # Start the download in a separate thread
    download_thread = threading.Thread(target=run_download)
    download_thread.start()

    # Start the monitor in a separate thread
    monitor_thread = threading.Thread(target=monitor_download)
    monitor_thread.start()

# Modify the queue_download function to pass the file size
def queue_download(file_links_dict, model_name):
    current_dir = Path(__file__).resolve().parent
    download_path = current_dir.resolve().parent / f"llama.cpp/models/{model_name.split('/')[-1]}"
    download_path.mkdir(parents=True, exist_ok=True)

    for file_name, file_info in file_links_dict.items():
        file_url, sha256_checksum = file_info['url'], file_info['sha256']
        # Check if file size is in file_info, otherwise get it from the file URL
        if 'size' in file_info:
            file_size = file_info['size']
        else:
            file_size = get_remote_file_size(file_url)  # Function to get file size
        
        download_task = partial(download_file_task, file_url, download_path, file_name, sha256_checksum, file_size, start_next_download)
        download_queue.append(download_task)

    start_next_download()
    return "Download tasks have been queued."



# Function to cancel all scheduled downloads
scheduled_jobs = []  # List to store scheduled jobs
downloaded_files = []  # List to store downloaded file paths

def cancel_downloads():
    global scheduled_jobs, downloaded_files
    for job in scheduled_jobs:
        job.remove()
    scheduled_jobs.clear()

    for file_path in downloaded_files:
        if os.path.exists(file_path):
            os.remove(file_path)
    downloaded_files.clear()

    return "All queued downloads have been canceled and files removed."
def get_remote_file_size(url):
    try:
        response = requests.head(url)
        response.raise_for_status()
        return int(response.headers.get('Content-Length', 0))
    except requests.RequestException as e:
        print(f"Error obtaining file size for {url}: {e}")
        return 0


def construct_hf_repo_url(model_name):
    base_url = "https://huggingface.co/api/models/"
    return f"{base_url}{model_name}/tree/main"

def get_files_from_repo(url, repo_name):
    file_info_dict = {}
    file_links_dict = {}

    try:
        response = requests.get(url)
        if response.status_code == 200:
            files_info = response.json()

            base_url = f"https://huggingface.co/{repo_name}/resolve/main/"
            for file in files_info:
                name = file.get('path', 'Unknown')
                size = file.get('size', 0)
                human_readable_size = f"{size / 1024 / 1024:.2f} MB"
                file_info_dict[name] = human_readable_size
                file_links_dict[name] = {
                    'url': base_url + name,
                    'sha256': file.get('sha256', '')
                }
    
    except Exception as e:
        print(f"Error obtaining files from repository: {e}")

    return file_info_dict, file_links_dict



# Old UI drawing
# def show_downloading_models_page():

st.title("Model Downloader")

# Streamlit UI to display download status
if st.button("Refresh Download Status"):
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as log_file:
            log_contents = log_file.read()
        st.text_area("Download Status", log_contents, height=300)
    else:
        st.write("No download status available yet.")

model_name = st.text_input("Download PyTorch models from Huggingface", "Use the HuggingfaceUsername/Modelname")
instruction = st.text("Instructions  . For example")
if st.button("Get File List"):
    file_info_dict, file_links_dict = get_files_from_repo(construct_hf_repo_url(model_name), model_name)
    if file_links_dict:

        files_info = "\n".join(f"{name}, Size: {file_info_dict[name]}" for name in file_links_dict)
        st.text_area("Files Information", files_info, height=300)
    else:
        st.error("Unable to retrieve file links.")
        if 'file_links_dict' in st.session_state:
            del st.session_state['file_links_dict']

if st.button("Download Files"):
    
    if 'file_links_dict' in st.session_state and st.session_state['file_links_dict']:
        queue_message = queue_download(st.session_state['file_links_dict'], model_name)
        st.text(queue_message)
        # Display download results if available
    if 'download_results' in st.session_state:
        for result in st.session_state['download_results']:
            st.write(result)

if st.button("Stop Downloads"):
    cancel_message = cancel_downloads()
    st.text(cancel_message)

with st.expander("How to Download Model Files from Hugging Face", expanded=False):
    st.markdown("""
    **How to Download Model Files from Hugging Face**

    - First, visit the Hugging Face model page that you want to download. For example, if you want to download the model at this link: [https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2).

    - On the model page, locate the icon next to the username of the model's author. This icon typically looks like a clipboard or a copy symbol. Click on this icon to copy the Username/RepositoryName, which in this example is `mistralai/Mistral-7B-Instruct-v0.2`.

    - Paste the copied Username/RepositoryName `mistralai/Mistral-7B-Instruct-v0.2` directly into the input field.

    - Click the "Get file list" button or option to retrieve the list of files available in this repository.

    - Review the list of files to ensure you have the correct model files that you want to download.

    - Finally, click the "Download Model" button or option to initiate the download process for the selected model files.

    - The model files will be saved in the `llama.cpp/models` directory on your device.

    - Now you have successfully downloaded the model files from Hugging Face, and they are stored in the `llama.cpp/models` directory for your use.
    """)

