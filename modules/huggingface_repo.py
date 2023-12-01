from huggingface_hub import HfApi
from requests.exceptions import HTTPError  # Correct import for HTTPError
from .token_encryption import decrypt_token
import gradio as gr

def get_username_from_token(token):
    """Get Hugging Face username from the provided token."""
    api = HfApi()
    user_info = api.whoami(token=token)
    return user_info['name']

def upload_folder_to_repo(encrypted_token, folder_path, default_repo_name="my-default-model-repo"):
    """
    Uploads a folder to a Hugging Face repository of type 'model', using an encrypted token.
    """
    try:
        # Decrypt the token
        decrypted_token = decrypt_token(encrypted_token)

        api = HfApi()

        # Get username from token
        username = get_username_from_token(decrypted_token)
        repo_id = f"{username}/{default_repo_name}"

        # Check if repository exists, if not, create it
        try:
            api.repo_info(repo_id=repo_id, token=decrypted_token)
        except HTTPError as e:
            if e.response.status_code == 404:
                # Create a new model repository if it does not exist
                api.create_repo(repo_id=repo_id, token=decrypted_token, repo_type="model")
            else:
                raise

        # Upload the folder
        upload_response = api.upload_folder(
            repo_id=repo_id,
            folder_path=folder_path,
            token=decrypted_token,
            repo_type="model"
        )

        return f"Folder uploaded successfully. View at: {upload_response}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def create_hf_repo_folder_upload_interface():
    """Create a Gradio interface for uploading a folder to a Hugging Face repository."""
    with gr.Blocks() as block:
        with gr.Row():
            gr.Markdown("### Upload Folder to Hugging Face Repository")
        with gr.Row():
            encrypted_token = gr.Textbox(label="Encrypted Hugging Face Token")
            folder_path = gr.Textbox(label="Path to Folder")
            default_repo_name = gr.Textbox(label="Repository Name", value="my-default-model-repo")
        with gr.Row():
            submit_btn = gr.Button("Upload Folder")
            output = gr.Textbox(label="Output", interactive=False)

        submit_btn.click(
            upload_folder_to_repo, 
            inputs=[encrypted_token, folder_path, default_repo_name], 
            outputs=output
        )

    return block

# Example to launch the interface:
# hf_repo_folder_upload_interface = create_hf_repo_folder_upload_interface()
# hf_repo_folder_upload_interface.launch()
