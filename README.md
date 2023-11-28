<img src="https://i.postimg.cc/ZKNgyLT0/chrome-Flwo-E6l-G9e.png" alt="Ollama Buddy" width="500" height="450" style="display: block; margin: 0 auto;">


# Ollama Companion

Welcome to **Ollama Companion**, a Gradio-based web application designed to streamline and simplify command line tasks for Ollama users. Our goal is to enhance the user experience by providing a user-friendly interface for managing and interacting with various models and functionalities.  
Want to try this companion without installing check out the notebook.  
https://github.com/Luxadevi/Ollama-Colab-Integration/tree/main
## Core Features

### Up-to-Date Model Access
- **Model Selection**: Easy access to an updated list of models through a user-friendly dropdown menu.

### ModelFile Templater
- **Parameter Customization**: Tailor model parameters like mirostat settings and temperature to your needs.
- **Simplified Deployment**: Deploy models with custom settings, bypassing complex command line processes.
- **Easy to use interface**: Visualize your modelfile with a UI and sliders for all parameters.  

### Detailed Model Insights
- **Model Information**: Access in-depth details about each model, including licensing and parameters.
- **Model Overview**: Quickly view all available models.

### Public Endpoint Management
- **Endpoint Control**: Manage public endpoints for Llama and OpenAI models with ease.
- **Log Monitoring**: Keep track of endpoint performance through real-time logs.
- **One click endpoint**: Get a public endpoint with just one buttonclick.
  

### LiteLLM Proxy Integration
- **Proxy Management**: Directly control the LiteLLM proxy via a simple interface.
- **Automated Polling**: Effortlessly implement polling for model updates.
- **Log Analysis**: Easily view and analyze LiteLLM proxy logs.
- **Dynamic Configuration**: Maintains a dynamically updated config for all models. Configurations are refreshed and the proxy is rebooted automatically when a new model is detected.

### Additional Utilities
- **CURL Command Creation**: Generate specific CURL commands for model interactions.
- **Manual Model Setup**: Directly create models with custom content and streaming.
- **Log File Handling**: Manage system logs for operational clarity.
  
## Coming Features in the Near Future

- **ChatUI with Custom Parameters**: An interactive ChatUI allowing for custom parameters to be set for each chat, enhancing user control and interaction flexibility.
- **Model Push Functionality**: A feature to push models directly from the interface, streamlining the process of model management.
- **Quantization and Automatic Push to GGUF and HuggingFace**: Automatically quantize different models and seamlessly push them to Ollama/HuggingFace repositories.
- **Embedding Generation**: Integrate the ability to generate embeddings, providing more depth to model interactions.
- **UI Improvement**: Add more general styling and colorscheme for the best readability

## Getting Started

### Automated Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Luxadevi/Ollama-Companion
   ```
2. Navigate to the cloned directory and run the `install.sh` script:
   ```bash
   cd Ollama-Companion
   ./install.sh
   ```

### Manual Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Luxadevi/Ollama-Companion
   ```
2. Navigate to the cloned directory:
   ```bash
   cd Ollama-Companion
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## System Requirements

- Python 3.x
- Necessary Python packages: `gradio`, `requests`, `flask`, `flask-cloudflared`, `httpx`, `yaml`, etc.
- LinuxOS


If someone could test this on MacOS and provide feedback so we can make the necessary changes

## Contributing

Contributions to Ollama Companion are highly appreciated. Please refer to our contributing guidelines for submitting pull requests and suggestions.

## License

Ollama Companion is available under [LICENSE]. It is free for use, modification, and distribution under the terms of the license.
