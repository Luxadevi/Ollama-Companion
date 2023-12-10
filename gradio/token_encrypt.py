import os
import streamlit as st
from cryptography.fernet import Fernet

# Function to load the existing key
def load_key():
    key_dir = os.path.join('.', '.key')
    key_file_path = os.path.join(key_dir, 'encryption.key')
    return open(key_file_path, "rb").read()

# Encrypt the token
def encrypt_token(token):
    key = load_key()
    f = Fernet(key)
    encrypted_token = f.encrypt(token.encode())
    return encrypted_token.decode()

def show_token_encrypt_page():
    st.title("Token Encryption")

    token = st.text_input("Enter your Hugging Face Token", type="password")

    if st.button("Encrypt Token"):
        if token:
            encrypted_token = encrypt_token(token)
            st.text_area("Encrypted Token", encrypted_token, height=100)
        else:
            st.error("Please enter a token to encrypt.")

# Uncomment this line to run this script directly for testing
show_token_encrypt_page()
