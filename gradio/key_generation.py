from cryptography.fernet import Fernet
import os

def generate_key():
    key_dir = os.path.join('.', '.key')
    key_file_path = os.path.join(key_dir, 'encryption.key')

    if not os.path.exists(key_file_path):
        key = Fernet.generate_key()
        if not os.path.exists(key_dir):
            os.makedirs(key_dir)
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)

# Call the function to ensure the key is generated when the module is imported
generate_key()
