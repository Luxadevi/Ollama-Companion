# main.py

import streamlit as st


@st.cache_data
def start_publicurl():
    cloudflared_cmd = 'pycloudflared', 'tunnel', '--url', 'http://127.0.0.1:8502'
    return cloudflared_cmd

start_publicurl()