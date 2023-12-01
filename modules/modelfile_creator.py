import gradio as gr
import requests
import json
import subprocess
from .shared import shared  # Import shared dictionary from shared.py

parameters = shared['parameters']


option_1_global = None
option_2_global = None
url = "https://raw.githubusercontent.com/Luxadevi/Ollama-Colab-Integration/main/models.json"
response = requests.get(url)
json_data = response.json()
options_1 = list(json_data.keys())  # ['mistral', 'llama2', 'codellama', ...]
options_2 = json_data  # The entire JSON data









def build_curl_command(model_name, modelfile_content, stop_sequence, *args):
    try:
        # Check if 'FROM' is present in the modelfile_content
        if 'FROM' not in modelfile_content:
            modelfile_content = f"FROM {option_1_global}:{option_2_global}" + modelfile_content

        for param, value in zip(parameters.keys(), args):
            default = parameters[param][0]
            if value != default:
                if param == 'mirostat':
                    modelfile_content += f"\nPARAMETER {['disabled', 'Mirostat 1', 'Mirostat 2.0'][value]}"
                else:
                    modelfile_content += f"\nPARAMETER {param} {value}"

        if stop_sequence:  # Add stop sequence if provided
            modelfile_content += f"\nPARAMETER stop {stop_sequence}"

        data = {
            "name": model_name,
            "modelfile": modelfile_content
        }
        curl_command = f"curl {shared['api_endpoint']['url']}/api/create -d '{json.dumps(data)}'"
        process = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
        return curl_command, process.stdout or process.stderr
    except Exception as e:
        return "", f"Error: {str(e)}"
def create_model_manually(model_name, modelfile_content, stream_response):
    try:
        data = {
            "name": model_name,
            "modelfile": modelfile_content,
            "stream": stream_response
        }
        response = requests.post(f"{shared['api_endpoint']['url']}/api/create", json=data)
        return response.json()
    except Exception as e:
        return {"curl_command": "", "execution_output": f"Error: {str(e)}"}
    

    

## Modelfilecreator interface
def create_modelfile_creator_interface():
    with gr.Blocks() as block:
        with gr.Tab("ModelFile Templater"):
            with gr.Row():
                model_name = gr.Textbox(label="Model Name", placeholder="Enter model name")
                modelfile_content_input = gr.Textbox(lines=10, label="Modelfile Content", placeholder="Enter modelfile content", scale=1)
                stop_sequence = gr.Textbox(label="Stop Sequence", placeholder="Enter stop sequence")



                with gr.Row():
                    parameter_inputs = []
                    for param, (default, range_) in parameters.items():
                        if isinstance(range_, list):  # Dropdown parameter
                            parameter_inputs.append(gr.Dropdown(label=param, choices=range_, value=default, scale=5))
                        elif range_ is None:  # Boolean parameter
                            parameter_inputs.append(gr.Checkbox(label=param, value=default, scale=5))
                        elif isinstance(range_, tuple):  # Numeric parameter with a range
                            parameter_inputs.append(
                                gr.Slider(label=param, minimum=range_[0], maximum=range_[1], value=default, scale=6, container=True))
            with gr.Row():
                d1 = gr.Dropdown(choices=options_1, label="Model-Provider")
                d2 = gr.Dropdown([],label="Model")

                def update_second(first_val):
                    d2 = gr.Dropdown(options_2[first_val])
                    return d2

                d1.input(update_second, d1, d2)

                outputs = gr.Textbox(label="Current model selected:")

                def print_results(option_1, option_2):
                    global option_1_global, option_2_global  # Declare them as global
                    option_1_global = option_1  # Update global variable
                    option_2_global = option_2  # Update global variable
                    return f"You selected '{option_1}:{option_2}' as the model to use."

                d2.input(print_results, [d1, d2], outputs)

            with gr.Row():    
                submit_button = gr.Button("Build and deploy Model")
                curl_command_output = gr.Textbox(label="API Call")
                execution_output = gr.Textbox(label="Execution Output", interactive=False)

                submit_button.click(
                    build_curl_command,
                    inputs=[model_name, modelfile_content_input, stop_sequence] + parameter_inputs,
                    outputs=[curl_command_output, execution_output]
                )
            return block        