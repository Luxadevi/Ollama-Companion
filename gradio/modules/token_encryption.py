import gradio as gr
from cryptography.fernet import Fernet
import os

# Function to load the existing key
def load_key():
    key_dir = os.path.join(os.path.dirname(__file__), '..', 'huggingface')
    key_file_path = os.path.join(key_dir, 'encryption.key')
    return open(key_file_path, "rb").read()

# Encrypt the token
def encrypt_token(token):
    key = load_key()
    f = Fernet(key)
    encrypted_token = f.encrypt(token.encode())
    return encrypted_token.decode()

# Decrypt the token
def decrypt_token(encrypted_token):
    key = load_key()
    f = Fernet(key)
    decrypted_token = f.decrypt(encrypted_token.encode()).decode()
    return decrypted_token

# Gradio function for encrypting token
def encrypt_interface(token):
    encrypted_token = encrypt_token(token)
    return encrypted_token

# Gradio function for decrypting token
def decrypt_interface(encrypted_token):
    try:
        decrypted_token = decrypt_token(encrypted_token)
        return decrypted_token
    except Exception as e:
        return f"Decryption failed: {str(e)}"

# Create Gradio interfaces for encryption and decryption
def create_token_encryption_interface():
    with gr.Blocks() as block:
        with gr.Tab("Encrypt Token"):
            token_input = gr.Textbox(label="Enter Hugging Face Token")
            encrypted_output = gr.Textbox(label="Encrypted Token", interactive=False)
            encrypt_button = gr.Button("Encrypt")
            encrypt_button.click(encrypt_interface, inputs=token_input, outputs=encrypted_output)

        with gr.Tab("Decrypt Token"):
            encrypted_input = gr.Textbox(label="Enter Encrypted Token")
            decrypted_output = gr.Textbox(label="Decrypted Token", interactive=False)
            decrypt_button = gr.Button("Decrypt")
            decrypt_button.click(decrypt_interface, inputs=encrypted_input, outputs=decrypted_output)

    return block
