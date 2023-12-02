import gradio as gr
from modules.high_ui import create_high_ui
from modules.mid_ui import create_mid_ui
from modules.low_ui import create_low_ui

def create_quant_ui():
    high_ui = create_high_ui()
    mid_ui = create_mid_ui()
    low_ui = create_low_ui()

    with gr.Blocks() as quant_ui:
        with gr.Tabs():
            with gr.Tab("High"):
                high_ui  # use high_ui directly
            with gr.Tab("Mid"):
                mid_ui  # use mid_ui directly
            with gr.Tab("Low"):
                low_ui  # use low_ui directly
    return quant_ui