import gradio as gr
from high_ui import create_high_ui
from mid_ui import create_mid_ui
from low_ui import create_low_ui

def create_quant_ui():
    high_ui = create_high_ui()
    mid_ui = create_mid_ui()
    low_ui = create_low_ui()

    with gr.Blocks() as quant_ui:
        with gr.Tabs():
            with gr.Tab("High"):
                high_ui()
            with gr.Tab("Mid"):
                mid_ui()
            with gr.Tab("Low"):
                low_ui()
    return quant_ui
