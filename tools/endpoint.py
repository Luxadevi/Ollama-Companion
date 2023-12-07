from time import time
from flask import Flask, request, Response
import requests
from flask_cloudflared import run_with_cloudflared
import gradio as gr
from threading import Thread
import sys
import os
import logging


# Add the parent directory (project) to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

# Import shared module from the "modules" directory
from modules.shared import shared

api_url = shared['api_endpoint']['url']
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    url = f'{api_url}/{path}'
    resp = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)
    print(f"request made on {api_url}/{path}")


    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]
    return Response(resp.content, resp.status_code, headers)

@app.route('/openai', defaults={'path': ''})
@app.route('/openai/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def openai_proxy(path):
    try:
        # Define the new URL for the openai proxy
        new_url = f'http://127.0.0.1:8000/{path}'
        print(f"dit is de link finaly {new_url}")
        # Log the URL for debugging
        logging.info(f"Proxying to URL: {new_url}")


        resp = requests.request(
            method=request.method,
            url=new_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]
        return Response(resp.content, resp.status_code, headers)
    except Exception as e:
        logging.error(f"Error in openai_proxy: {e}")
        return Response(f"Error: {e}", status=500)

run_with_cloudflared(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
