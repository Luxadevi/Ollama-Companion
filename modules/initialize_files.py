import os
from cryptography.fernet import Fernet
import yaml
from .shared import shared
# creates 2 folders in root folder one for logs and one for configs


# Creates logfiles
def initialize_log_files():
    log_files = ["litellmlog", "endpoint.log", "endpoint_openai.log"]
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')  # Adjust the path as necessary

    os.makedirs(log_dir, exist_ok=True)  

    for log_file in log_files:
        log_file_path = os.path.join(log_dir, log_file)
        if not os.path.exists(log_file_path):
            open(log_file_path, 'w').close()
            print(f"Created log file: {log_file_path}")
        else:
            print(f"Log file already exists: {log_file_path}")

# Creates config files
def initialize_config_file():
    config_dir = os.path.join(os.path.dirname(__file__), '..', 'configs')  # Adjust the path as necessary
    os.makedirs(config_dir, exist_ok=True)  # Create the configs directory if it doesn't exist
    config_file_path = os.path.join(config_dir, 'config.yaml')

    if not os.path.exists(config_file_path):
        config_data = {
            "model_list": [
                {
                    "model_name": "ollama/dummyentry",
                    "litellm_params": {
                        "model": "ollama/dummyentry",
                        "api_base": shared['api_endpoint']['url'],  
                        "json": True
                    }
                }
            ]
        }
        with open(config_file_path, 'w') as file:
            yaml.dump(config_data, file, default_flow_style=False, sort_keys=False)
        print(f"Created configuration file: {config_file_path}")
    else:
        print(f"Configuration file already exists: {config_file_path}")




def initialize_encryption_key():
    key_dir = os.path.join(os.path.dirname(__file__), '..', 'huggingface')
    os.makedirs(key_dir, exist_ok=True)  # Create the huggingface directory if it doesn't exist
    key_file_path = os.path.join(key_dir, 'encryption.key')

    if not os.path.exists(key_file_path):
        key = Fernet.generate_key()
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)
        print(f"Created encryption key file: {key_file_path}")
    else:
        print(f"Encryption key file already exists: {key_file_path}")

def initialize_files():
    initialize_log_files()
    initialize_config_file()
    initialize_encryption_key()