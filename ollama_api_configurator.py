# ollama_api_configurator.py

import streamlit as st
from shared import shared  # Importing the shared dictionary

def update_shared_file(new_url):
    try:
        # Read the current contents of the file
        with open('shared.py', 'r') as file:
            lines = file.readlines()

        # Find and modify the api_endpoint line
        for i, line in enumerate(lines):
            if line.strip().startswith("'api_endpoint':"):
                start = line.find('{')
                end = line.rfind('}') + 1
                dict_str = line[start:end]
                shared_dict = eval(dict_str)  # Using eval to convert string to dict
                shared_dict['url'] = new_url  # Modify the url
                new_line = f"    'api_endpoint': {shared_dict},\n"
                lines[i] = new_line
                break

        # Write the modified contents back to the file
        with open('shared.py', 'w') as file:
            file.writelines(lines)

        return "API Endpoint URL updated successfully!"
    except Exception as e:
        return f"Error: {e}"

def show_ollama_api_configurator():
    st.title("Ollama API Configuration")

    # Display and allow editing of the API endpoint URL
    current_url = st.text_input("API Endpoint URL", value=shared['api_endpoint']['url'])

    if st.button("Update"):
        message = update_shared_file(current_url)
        st.success(message)

        # Optionally, display the updated URL
        st.write("Updated API Endpoint URL:", current_url)
