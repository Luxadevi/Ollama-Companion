import streamlit as st
from model_selector import show_model_selector
from modelfile_templater import show_model_dropdowns, show_parameter_sliders, show_model_name_input, display_curl_command
from ollama_api_configurator import show_ollama_api_configurator
from litellm_proxy import show_litellm_proxy_page
from public_endpoint import show_public_endpoint_page
from downloading_models import show_downloading_models_page
from High_Precision_Quantization import show_high_precision_quantization_page
from Medium_Precision_Quantization import show_medium_precision_quantization_page
from model_management import show_model_management_page  
from token_encrypt import show_token_encrypt_page
import key_generation


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a Page", ["Model Selector", "Modelfile Templater", "Ollama-API", 
                                              "LiteLLM Proxy", "Public Endpoint", "Downloading Models",
                                              "High Precision Quantization", "Medium Precision Quantization",
                                              "Model Management", "Token-encrypt"])

    if page == "Model Selector":
        show_model_selector()
    elif page == "Modelfile Templater":
        show_model_name_input()
        show_model_dropdowns()
        show_parameter_sliders()
        display_curl_command()
    elif page == "Ollama-API":
        show_ollama_api_configurator()
    elif page == "LiteLLM Proxy":
        show_litellm_proxy_page()
    elif page == "Public Endpoint":
        show_public_endpoint_page()
    elif page == "Downloading Models":
        show_downloading_models_page()
    elif page == "High Precision Quantization":
        show_high_precision_quantization_page()
    elif page == "Medium Precision Quantization":
        show_medium_precision_quantization_page()
    elif page == "Model Management": 
        show_model_management_page()
    elif page == "Token-encrypt":
        show_token_encrypt_page()


if __name__ == "__main__":
    main()
