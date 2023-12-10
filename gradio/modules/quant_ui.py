import gradio as gr
from modules.high_ui import create_high_ui 
from modules.mid_ui import create_mid_ui
from modules.low_ui import create_low_ui

def create_quant_ui():
    with gr.Blocks() as quant_ui:
        with gr.Tabs():
            with gr.Tab("High"):
                create_high_ui()  # Call the function to create high_ui
            with gr.Tab("Mid"):
                create_mid_ui()  # Call the function to create mid_ui
            with gr.Tab("Low"):
                create_low_ui()  # Call the function to create low_ui
    return quant_ui
