import os
import streamlit as st
from huggingface_hub import HfApi
from requests.exceptions import HTTPError
from cryptography.fernet import Fernet
from token_encrypt import load_key

## Uses username from HF Token
def get_username_from_token(token):
    api = HfApi()
    user_info = api.whoami(token=token)
    return user_info['name']

## Decrypt token if used encrypted token
def decrypt_token(encrypted_token):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_token.encode()).decode()

def upload_files_to_repo(token, models_dir, repo_name, files_to_upload, readme_content, high_precision_files, medium_precision_files, selected_model):
    try:
        api = HfApi()
        username = get_username_from_token(token)
        repo_id = f"{username}/{repo_name}"

        # Check if the repository exists, if not create it
        try:
            api.repo_info(repo_id=repo_id, token=token)
        except HTTPError as e:
            if e.response.status_code == 404:
                api.create_repo(repo_id=repo_id, token=token, repo_type="model")
            else:
                raise

        # Upload README.md if content is provided
        if readme_content:
            readme_path = os.path.join(models_dir, 'README.md')
            with open(readme_path, 'w') as readme_file:
                readme_file.write(readme_content)
            api.upload_file(path_or_fileobj=readme_path, path_in_repo='README.md', repo_id=repo_id, token=token)
            os.remove(readme_path)

        # Upload selected files
        for file_name in files_to_upload:
            if file_name in high_precision_files.get(selected_model, []):
                folder_path = os.path.join(models_dir, selected_model, "High-Precision-Quantization")
            elif file_name in medium_precision_files.get(selected_model, []):
                folder_path = os.path.join(models_dir, selected_model, "Medium-Precision-Quantization")
            else:
                continue  # Skip if the file is not found in either folder

            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                api.upload_file(path_or_fileobj=file_path, path_in_repo=file_name, repo_id=repo_id, token=token)

        return f"Files uploaded successfully. View at: https://huggingface.co/{repo_id}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def list_model_files(models_dir, subfolder):
    model_files = {}
    if os.path.exists(models_dir):
        for model_folder in os.listdir(models_dir):
            specific_folder = os.path.join(models_dir, model_folder, subfolder)
            if os.path.exists(specific_folder) and os.path.isdir(specific_folder):
                model_files[model_folder] = os.listdir(specific_folder)
    return model_files

def show_model_management_page():
    st.title("Model Management")

    models_dir = "llama.cpp/models/"
    high_precision_files = list_model_files(models_dir, "High-Precision-Quantization")
    medium_precision_files = list_model_files(models_dir, "Medium-Precision-Quantization")

    # Initialize session state for file selection
    if 'selected_files' not in st.session_state:
        st.session_state['selected_files'] = []

    selected_model = st.selectbox("Select a Model", list(set(high_precision_files.keys()) | set(medium_precision_files.keys())))

    suggested_repo_name = f"{selected_model}-GGUF"
    repo_name = st.text_input("Repository Name", value=suggested_repo_name)
    st.caption("Suggested name: " + suggested_repo_name + " (Suggestion)")

    # Display current subfolder's files along with the already selected files
    selected_subfolder = st.radio("Select a Subfolder", ["High-Precision-Quantization", "Medium-Precision-Quantization"])
    current_files = high_precision_files.get(selected_model, []) if selected_subfolder == "High-Precision-Quantization" else medium_precision_files.get(selected_model, [])
    all_files = list(set(current_files) | set(st.session_state['selected_files']))
    
    selected_files_to_upload = st.multiselect("Select Files to Upload", all_files, default=st.session_state['selected_files'])
    st.session_state['selected_files'] = selected_files_to_upload

    readme_content = st.text_area("README.md Content", "Enter content for README.md")

    use_unencrypted_token = st.checkbox("Unencrypted Token")
    hf_token = ""
    if use_unencrypted_token:
        hf_token = st.text_input("Hugging Face Token", type="password")
    else:
        encrypted_token = st.text_input("Enter Encrypted Token", type="password")
        if encrypted_token:
            hf_token = decrypt_token(encrypted_token)
            os.environ['HUGGINGFACE_TOKEN'] = hf_token

    if st.button("Upload Selected Files"):
        folder_to_upload = os.path.join(models_dir, selected_model, selected_subfolder)
        upload_message = upload_files_to_repo(
            hf_token, 
            models_dir, 
            repo_name, 
            st.session_state['selected_files'], 
            readme_content, 
            high_precision_files, 
            medium_precision_files, 
            selected_model
        )
        st.text(upload_message)

        if 'HUGGINGFACE_TOKEN' in os.environ:
            del os.environ['HUGGINGFACE_TOKEN']
