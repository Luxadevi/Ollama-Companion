# main.py
import gradio as gr
from modules.model_info import create_model_info_interface
from modules.modelfile_creator import create_modelfile_creator_interface
from modules.api_config import create_api_config_interface
from modules.litellm_proxy import create_litellm_proxy_interface
from modules.initialize_files import initialize_files  # Import the initialization function
from modules.public_endpoint import create_public_endpoint_interface
from modules.huggingface_repo import create_hf_repo_interface  # Updated import
from modules.token_encryption import create_token_encryption_interface  # Assuming this is your token encryption interface

def main():
    # Initialization (this will also handle key generation)
    initialize_files()

    # Creating interfaces from modules
    model_info_interface = create_model_info_interface()
    model_file_creator_interface = create_modelfile_creator_interface()
    api_config_interface = create_api_config_interface()
    litellm_proxy_interface = create_litellm_proxy_interface()
    public_endpoint_interface = create_public_endpoint_interface()
    token_encryption_interface = create_token_encryption_interface()
    hf_repo_interface = create_hf_repo_interface()

    # Tabbed Interface
    gr.TabbedInterface(
        [model_info_interface, model_file_creator_interface, api_config_interface, 
         litellm_proxy_interface, public_endpoint_interface, hf_repo_interface, token_encryption_interface],
        ["Model Info", "ModelFile Templater", "API Configuration", 
         "LiteLLM-Proxy", "Public Endpoint", "Hugging Face Repo", "Token Encryption"]
    ).launch(server_name="0.0.0.0", server_port=7860, share=True)

if __name__ == "__main__":
    main()
