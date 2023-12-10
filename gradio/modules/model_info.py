# model_info.py
import json
import subprocess
import requests
import gradio as gr
from .shared import shared  # Adjust the import path as necessary

def show_model_details(model_name):
    api_url = shared['api_endpoint']['url']
    curl_command = f"curl {api_url}/api/show -d '{{\"name\": \"{model_name}\"}}'"
    process = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    output = process.stdout or process.stderr

    try:
        json_data = json.loads(output)
        license_info = json_data.get('license', 'Not available')
        modelfile_info = json_data.get('modelfile', 'Not available')
        parameters_info = json.dumps(json_data.get('parameters', {}), indent=4)
        template_info = json_data.get('template', 'Not available')
        return license_info, modelfile_info, parameters_info, template_info
    except json.JSONDecodeError:
        return (output, "", "", "")

def list_models():
    api_url = shared['api_endpoint']['url']
    url = f"{api_url}/api/tags"
    response = requests.get(url)
    models = response.json().get('models', [])
    return "\n".join([model['name'] for model in models])

def create_model_info_interface():
    with gr.Blocks() as block:
        with gr.Tab("Model Info"):
            with gr.Row():
                shared['gradio']['model_name_input'] = gr.Textbox(label="Model Name", placeholder="Enter model name for details")
                shared['gradio']['model_info_button'] = gr.Button("Get Model Info")
                shared['gradio']['model_list_button'] = gr.Button("List All Models")

            shared['gradio']['license_output'] = gr.Textbox(label="License", interactive=False)
            shared['gradio']['modelfile_output'] = gr.Textbox(label="Modelfile", interactive=False)
            shared['gradio']['parameters_output'] = gr.Textbox(label="Parameters", interactive=False)
            shared['gradio']['template_output'] = gr.Textbox(label="Template", interactive=False)
            shared['gradio']['model_list_output'] = gr.Textbox(label="List of Models", interactive=False)

            shared['gradio']['model_info_button'].click(
                fn=show_model_details,
                inputs=[shared['gradio']['model_name_input']],
                outputs=[shared['gradio']['license_output'], shared['gradio']['modelfile_output'], shared['gradio']['parameters_output'], shared['gradio']['template_output']]
            )

            shared['gradio']['model_list_button'].click(
                fn=list_models,
                inputs=[],
                outputs=[shared['gradio']['model_list_output']]
            )

        return block
