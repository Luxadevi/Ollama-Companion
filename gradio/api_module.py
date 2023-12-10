# api_module.py
import streamlit as st
import requests

@st.cache
def get_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return str(e)

def show_model_details(model_name, api_url):
    try:
        response = requests.post(f"{api_url}/api/show", json={"name": model_name})
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return str(e)