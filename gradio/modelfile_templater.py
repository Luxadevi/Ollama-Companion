# modelfile_templater.py

import streamlit as st
import requests
import json
from shared import shared  # Make sure this import works with your project structure

def load_model_data():
    url = "https://raw.githubusercontent.com/Luxadevi/Ollama-Colab-Integration/main/models.json"
    response = requests.get(url)
    return response.json()

def show_model_dropdowns():
    json_data = load_model_data()
    if json_data:
        model_providers = list(json_data.keys())
        selected_provider = st.selectbox("Select Model Provider", model_providers)

        if selected_provider:
            models = json_data[selected_provider]
            selected_model = st.selectbox("Select Model", models)
        else:
            selected_model = None

        st.session_state['selected_provider'] = selected_provider
        st.session_state['selected_model'] = selected_model
    else:
        st.error("Failed to load model data.")

def show_parameter_sliders():
    for param, value in shared['parameters'].items():
        default, range_ = value
        if isinstance(range_, list):  # Dropdown parameter
            st.session_state[param] = st.selectbox(param, range_, index=default)
        else:  # Slider parameter
            min_val, max_val = range_
            st.session_state[param] = st.slider(param, min_value=min_val, max_value=max_val, value=default)

def show_model_name_input():
    st.session_state['model_name'] = st.text_input("Model Name", placeholder="Enter model name")

def build_curl_command():
    # Start with the FROM clause
    modelfile_content = f"FROM {st.session_state.get('selected_provider', '')}:{st.session_state.get('selected_model', '')}\n"

    # Append PARAMETER lines for each parameter where the user has changed the default value
    for param, value in shared['parameters'].items():
        default, _ = value
        current_value = st.session_state.get(param)
        if current_value is not None and current_value != default:
            modelfile_content += f"PARAMETER {param} {current_value}\n"

    # Constructing the CURL command
    model_name = st.session_state.get('model_name', 'default_model_name')
    api_url = shared['api_endpoint']['url']
    data = json.dumps({"name": model_name, "modelfile": modelfile_content})
    curl_command = f"curl {api_url}/api/create -d '{data}'"

    return curl_command

# Add a function to display the CURL command in the Streamlit app
def display_curl_command():
    if st.button("Generate CURL Command"):
        curl_command = build_curl_command()
        st.text_area("CURL Command", curl_command, height=100)