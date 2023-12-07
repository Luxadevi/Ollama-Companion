import gradio as gr
import random
import time
import requests
import json
# Chat logic
def respond(message, chat_history):
    # Data to be sent in POST request
    data = {
        "model": "nextgen",
        "prompt": message
    }
    # Making the POST request
    response = requests.post("http://127.0.0.1:11434/api/generate", json=data)
    
    bot_message = ""
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:  # avoid keep-alive new lines
                json_response = json.loads(line)
                bot_message += json_response.get("response", "")
                if json_response.get("done", False):
                    break
    else:
        bot_message = "Error in generating response"

    chat_history.append((message, bot_message))
    return "", chat_history


def create_chat_ui():
    with gr.Blocks() as block:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("Clear")

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot)
    return block
