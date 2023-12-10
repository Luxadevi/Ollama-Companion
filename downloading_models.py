import os
import subprocess
import streamlit as st
import requests
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize APScheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Global variables to keep track of download tasks and downloaded files
scheduled_jobs = []
downloaded_files = []

def download_file_task(file_url, download_path, filename):
    global downloaded_files
    file_path = os.path.join(download_path, filename)
    command = [
        "aria2c", file_url,
        "--max-connection-per-server=16", "--split=8", "--min-split-size=25M", "--allow-overwrite=true",
        "-d", download_path, "-o", filename,
        "--continue=true"
    ]
    try:
        subprocess.run(command, check=True)
        downloaded_files.append(file_path)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {filename}: {str(e)}")

def queue_download(file_links_dict, model_name):
    global scheduled_jobs
    folder_name = model_name.split("/")[-1]
    download_path = f"llama.cpp/models/{folder_name}"
    os.makedirs(download_path, exist_ok=True)

    for file_name, file_url in file_links_dict.items():
        filename = file_name.split('/')[-1]
        job = scheduler.add_job(download_file_task, args=[file_url, download_path, filename])
        scheduled_jobs.append(job)

    return "Download tasks have been queued."

def cancel_downloads():
    global scheduled_jobs, downloaded_files
    for job in scheduled_jobs:
        job.remove()
    scheduled_jobs.clear()

    for file_path in downloaded_files:
        if os.path.exists(file_path):
            os.remove(file_path)
    downloaded_files.clear()

    return "All queued downloads have been cancelled and files removed."

def construct_hf_repo_url(model_name):
    base_url = "https://huggingface.co/api/models/"
    return f"{base_url}{model_name}/tree/main"

def get_files_from_repo(url, repo_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            files_info = response.json()
            file_info_dict = {}
            file_links_dict = {}

            base_url = f"https://huggingface.co/{repo_name}/resolve/main/"
            for file in files_info:
                name = file.get('path', 'Unknown')
                size = file.get('size', 0)
                human_readable_size = f"{size / 1024 / 1024:.2f} MB"
                file_info_dict[name] = human_readable_size
                file_links_dict[name] = base_url + name

            return file_info_dict, file_links_dict
        else:
            return {}, {}
    except Exception as e:
        return {}, {}

def show_downloading_models_page():
    st.title("Model Downloader")

    model_name = st.text_input("Model Name or ID", "Enter a model name")

    if st.button("Get File List"):
        _, file_links = get_files_from_repo(construct_hf_repo_url(model_name), model_name)
        if file_links:
            st.session_state['file_links_dict'] = file_links
            files_info = "\n".join(f"{name}, Size: {size}" for name, size in file_links.items())
            st.text_area("Files Information", files_info, height=300)
        else:
            st.error("Unable to retrieve file links.")
            if 'file_links_dict' in st.session_state:
                del st.session_state['file_links_dict']

    if st.button("Download Files"):
        if 'file_links_dict' in st.session_state and st.session_state['file_links_dict']:
            queue_message = queue_download(st.session_state['file_links_dict'], model_name)
            st.text(queue_message)
        else:
            st.error("No files to download. Please get the file list first.")

    if st.button("Stop Downloads"):
        cancel_message = cancel_downloads()
        st.text(cancel_message)
