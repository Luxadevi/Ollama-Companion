# model_selector.py

import streamlit as st
from api_module import get_json, show_model_details
from shared import shared
def show_model_selector():
    st.title('Model Selector')

    api_url = shared['api_endpoint']['url']  # Replace with your API URL
    if 'model_names' not in st.session_state:
        st.session_state['model_names'] = []

    fetch_button = st.button('Fetch Models')
    if fetch_button:
        json_data = get_json(f"{api_url}/api/tags")
        if isinstance(json_data, dict) and 'models' in json_data:
            st.session_state['model_names'] = [model['name'] for model in json_data['models']]
        else:
            st.error("Invalid JSON structure or error in fetching data")

    if st.session_state['model_names']:
        selected_model = st.selectbox("Select a Model", st.session_state['model_names'])
        if st.button('Show Model Details'):
            details = show_model_details(selected_model, api_url)
            st.text_area("Model Details", value=details, height=300)