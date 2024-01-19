# main.py
import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, add_indentation


show_pages(
    [
    Page("Homepage.py", "Home", ":house:"),
    Page("pages/Docs.py", "Docs", ":books:"),
    Page("pages/Chat_Interface.py", "Chat Interface", ":speech_balloon:"),
    Page("pages/OpenAI_LiteLLM.py", "OpenAI compatibility", ":robot_face:"),
    Page("pages/Public_Endpoint.py", "Generate public url", ":globe_with_meridians:"),
    Section("Ollama Management", icon=":llama:"),
    Page("pages/Modelfile_Creator.py", "Create and download models", ":wrench:", in_section=True),
    Page("pages/Model_Info.py", "Remove or view models", ":clipboard:"),
    Page("pages/Ollama_Endpoint_Url.py", "Set Ollama network address", ":signal_strength:"),
    Section("Manually convert models", icon=":arrows_counterclockwise:"),
    Page("pages/Hugging_Face_Downloader.py", "Download model", ":inbox_tray:"),
    Page("pages/High_Precision_Quantization.py", "High Precision Quantization", ":gem:"),
    Page("pages/Medium_Precision_Quantization.py", "Medium Precision Quantization", ":heavy_plus_sign:" ),
    Page("pages/Upload_Converted_To_HF.py", "Upload model to HuggingFace", ":outbox_tray:"),
    Section("Extra Tools", icon=":toolbox:"),
    Page("pages/HF_Token_Encrypter.py", "Security", ":lock:"),
    ]    
)

add_indentation()



st.markdown(""" 
# Welcome to Ollama-Companion.  
---
Thank you for installing the Ollama-Companion, to get started use the sidebar to navigate to the page you want to use,  
if you have any question sor want to learn how to use a certain functionality then navigate to the ***"Docs"*** page located within the sidebar.""")

