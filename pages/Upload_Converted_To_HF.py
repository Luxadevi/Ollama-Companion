import os
import streamlit as st
from huggingface_hub import HfApi
from requests.exceptions import HTTPError
from cryptography.fernet import Fernet
from pages.HF_Token_Encrypter import load_key
from pathlib import Path  # Import pathlib

# Initialize session state for selected_model
if 'selected_model' not in st.session_state:
    st.session_state['selected_model'] = ''
if 'selected_files' not in st.session_state:
    st.session_state['selected_files'] = []

# Define a function to search for the llama.cpp directory
def find_llama_cpp_dir():
    # Search for llama.cpp directory three levels up
    current_dir = Path(__file__).resolve().parent
    for _ in range(3):
        current_dir = current_dir.parent
        llama_cpp_dir = current_dir / 'llama.cpp'
        models_dir = llama_cpp_dir / "models"
        if llama_cpp_dir.is_dir():
            return llama_cpp_dir, models_dir

    # If not found, search two levels down
    current_dir = Path(__file__).resolve().parent
    for _ in range(2):
        current_dir = current_dir / 'llama.cpp'
        models_dir = current_dir / "models"
        if current_dir.is_dir():
            return current_dir, models_dir

    return None, None

# Search for the llama.cpp directory
llama_cpp_dir, models_dir = find_llama_cpp_dir()
if not llama_cpp_dir:
    st.error("llama.cpp directory not found. Please check the file structure.")




## Uses username from HF Token
def get_username_from_token(token):
    api = HfApi()
    user_info = api.whoami(token=token)
    return user_info['name']

# Decrypt the token
def decrypt_token(encrypted_token):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_token.encode()).decode()


# Gathers files and uploads to HuggingFace
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
            readme_path = Path(models_dir) / 'README.md'
            with open(str(readme_path), 'w') as readme_file:
                readme_file.write(readme_content)
            api.upload_file(path_or_fileobj=str(readme_path), path_in_repo='README.md', repo_id=repo_id, token=token)
            os.remove(str(readme_path))

        # Upload selected files
        for file_name in files_to_upload:
            if file_name in high_precision_files.get(selected_model, []):
                folder_path = Path(models_dir) / selected_model / "High-Precision-Quantization"
            elif file_name in medium_precision_files.get(selected_model, []):
                folder_path = Path(models_dir) / selected_model / "Medium-Precision-Quantization"
            else:
                continue

            file_path = folder_path / file_name
            if file_path.is_file():
                api.upload_file(path_or_fileobj=str(file_path), path_in_repo=file_name, repo_id=repo_id, token=token)

        return f"Files uploaded successfully. View at: https://huggingface.co/{repo_id}"
    except Exception as e:
        return f"An error occurred: {str(e)}"



# Cache the function to improve performance
@st.cache_data
def list_model_files(models_dir, subfolder):
    model_files = {}
    models_dir_path = Path(models_dir)
    if models_dir_path.exists() and models_dir_path.is_dir():
        for model_folder in models_dir_path.iterdir():
            specific_folder = model_folder / subfolder
            if specific_folder.exists() and specific_folder.is_dir():
                model_files[model_folder.name] = [file.name for file in specific_folder.iterdir() if file.is_file()]
    return model_files

# List files in High-Precision and Medium-Precision folders
high_precision_files = list_model_files(models_dir, "High-Precision-Quantization")
medium_precision_files = list_model_files(models_dir, "Medium-Precision-Quantization")

# After calling list_model_files, check the contents
# print("High Precision Files:", high_precision_files)
# print("Medium Precision Files:", medium_precision_files)

# Old UI drawing
# def show_model_management_page():
# Search for the llama.cpp directory
# llama_cpp_dir = find_llama_cpp_dir()
# models_dir = "llama.cpp/models/"
# high_precision_files = list_model_files(models_dir, "High-Precision-Quantization")
# medium_precision_files = list_model_files(models_dir, "Medium-Precision-Quantization")


def get_combined_files(model):
    # Combine files from both precision types
    return high_precision_files.get(model, []) + medium_precision_files.get(model, [])

# Main UI
st.title("Upload Converted Models to HuggingFace")

# Select a model
all_models = list(set(high_precision_files.keys()) | set(medium_precision_files.keys()))
selected_model = st.selectbox("Select a Model", all_models, index=0)

# File selection multiselect
combined_files = get_combined_files(selected_model)
selected_files = st.multiselect("Select Files to Upload", combined_files, key="file_selector")


# Repository details and README content
repo_name = st.text_input("Repository Name", value=f"{selected_model}-GGUF")
readme_content = st.text_area("README.md Content", "Enter content for README.md")

# Token input
use_unencrypted_token = st.checkbox("Unencrypted Token")
if use_unencrypted_token:
    hf_token = st.text_input("Hugging Face Token", type="password")
else:
    encrypted_token = st.text_input("Enter Encrypted Token", type="password")
    if encrypted_token:
        hf_token = decrypt_token(encrypted_token)

# Upload button
if st.button("Upload Selected Files") and hf_token:
    upload_message = upload_files_to_repo(
        token=hf_token, 
        models_dir=models_dir, 
        repo_name=repo_name, 
        files_to_upload=selected_files, 
        readme_content=readme_content,
        high_precision_files=high_precision_files,
        medium_precision_files=medium_precision_files,
        selected_model=selected_model
    )
    st.info(upload_message)

if 'HUGGINGFACE_TOKEN' in os.environ:
    del os.environ['HUGGINGFACE_TOKEN']

with st.expander("Model Upload Instructions", expanded=False):
    st.markdown("""
    **Model Upload Instructions**

    Use this section to upload your converted models to Hugging Face with enhanced security.

    **Steps for Uploading Models:**

    1. **Select a Model:** Choose a model from the dropdown list. These models are found in the `llama.cpp/models` directory.
    2. **Enter Repository Name:** Specify a name for the new Hugging Face repository where your model will be uploaded.
    3. **Choose Files for Upload:** Select the files you want to upload from the chosen model's subfolders.
    4. **Add README Content:** Optionally, write content for the README.md file of your repository.
    5. **Token Usage:**
        - For added security, use an encrypted token. Encrypt your Hugging Face token on the **Token Encrypt** page and paste it into the "Enter Encrypted Token" field.
        - Alternatively, you can directly enter an unencrypted Hugging Face token.
    6. **Upload Files:** Click the "Upload Selected Files" button to start uploading your files to Hugging Face.

    The uploaded models will be viewable at `https://huggingface.co/your-username/your-repo-name`.
    """)
