import gradio as gr
from .shared import shared

def create_api_config_interface():
    with gr.Blocks() as block:
        with gr.Tab("API Configuration"):
            with gr.Row():
                api_input = gr.Textbox(label="API Endpoint URL", value=shared['api_endpoint']['url'])
                update_button = gr.Button("Update API Endpoint")

                def update_api_endpoint(new_url):
                    shared['api_endpoint']['url'] = new_url
                    return "API Endpoint updated successfully!"

                update_button.click(update_api_endpoint, inputs=api_input, outputs=None)

        return block