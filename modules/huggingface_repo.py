from huggingface_hub import HfApi
from requests.exceptions import HTTPError
import gradio as gr
import subprocess
import requests
import json
import os

# Assuming the token_encryption module provides a decrypt_token function
from .token_encryption import decrypt_token

def get_username_from_token(token):
    api = HfApi()
    user_info = api.whoami(token=token)
    return user_info['name']

def upload_folder_to_repo(encrypted_token, folder_path, default_repo_name="my-default-model-repo"):
    try:
        decrypted_token = decrypt_token(encrypted_token)
        api = HfApi()
        username = get_username_from_token(decrypted_token)
        repo_id = f"{username}/{default_repo_name}"

        try:
            api.repo_info(repo_id=repo_id, token=decrypted_token)
        except HTTPError as e:
            if e.response.status_code == 404:
                api.create_repo(repo_id=repo_id, token=decrypted_token, repo_type="model")
            else:
                raise

        upload_response = api.upload_folder(repo_id=repo_id, folder_path=folder_path, token=decrypted_token, repo_type="model")
        return f"Folder uploaded successfully. View at: {upload_response}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def download_files(file_links_dict, model_name):
    folder_name = model_name.split("/")[-1]
    download_path = f"llama.cpp/models/{folder_name}"

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for file_name, file_url in file_links_dict.items():
        # Extract the filename from the file_name
        filename = file_name.split('/')[-1]

        try:
            subprocess.run([
                "aria2c", file_url,
                "--max-connection-per-server=16", "--split=12", "--min-split-size=5M",
                "-d", download_path, "-o", filename,  # Specify output filename
                "--continue=true"  # To resume download if it stops
            ], check=True)
        except Exception as e:
            return f"An error occurred during downloading {filename}: {str(e)}"
    return f"Files downloaded successfully to {download_path}."


def download_process(model_name):
    _, file_links_dict = get_files_from_repo(construct_hf_repo_url(model_name), model_name)
    if file_links_dict:
        return download_files(file_links_dict, model_name)
    else:
        return "Error: Unable to retrieve file links."

def download_from_url(url):
    try:
        subprocess.run(["aria2c", url], check=True)
        return f"Downloaded successfully from {url}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

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

def create_hf_repo_interface():
    with gr.Blocks() as block:
        with gr.Tab("Upload to Hugging Face"):
            with gr.Row():
                gr.Markdown("### Upload Folder to Hugging Face Repository")
            with gr.Row():
                encrypted_token = gr.Textbox(label="Encrypted Hugging Face Token")
                folder_path = gr.Textbox(label="Path to Folder")
                default_repo_name = gr.Textbox(label="Repository Name", value="my-default-model-repo")
            with gr.Row():
                upload_btn = gr.Button("Upload Folder")
                upload_output = gr.Textbox(label="Output", interactive=False)

            upload_btn.click(upload_folder_to_repo, inputs=[encrypted_token, folder_path, default_repo_name], outputs=upload_output)

        with gr.Tab("Download from URL"):
            with gr.Row():
                gr.Markdown("### Download Files")
            with gr.Row():
                url_input = gr.TextArea(label="Enter URL")
                download_btn = gr.Button("Download")
                download_output = gr.Textbox(label="Output", interactive=False)

            download_btn.click(download_from_url, inputs=[url_input], outputs=[download_output])

        with gr.Tab("Model Downloader"):
            with gr.Row():
                gr.Markdown("### Download Models from Hugging Face")
            with gr.Row():
                model_name_input = gr.Textbox(label="Model Name or ID")
            with gr.Row():
                files_info_output = gr.TextArea(label="Files Information", interactive=False)
                download_files_output = gr.Textbox(label="Output", interactive=False)
            with gr.Row():
                get_files_btn = gr.Button("Get File List")
                download_files_btn = gr.Button("Download Files")

                get_files_btn.click(lambda model_name: "\n".join(f"{name}, Size: {size}" for name, size in get_files_from_repo(construct_hf_repo_url(model_name), model_name)[0].items()), inputs=[model_name_input], outputs=[files_info_output])
                download_files_btn.click(download_process, inputs=[model_name_input], outputs=[download_files_output])

    return block

if __name__ == "__main__":
    iface = create_hf_repo_interface()
    iface.launch()
