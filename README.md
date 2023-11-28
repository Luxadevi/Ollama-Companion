<img src="https://i.postimg.cc/ZKNgyLT0/chrome-Flwo-E6l-G9e.png" alt="Ollama Buddy" width="500" height="450" style="display: block; margin: 0 auto;">


# Ollama Companion

Welcome to **Ollama Companion**, a Gradio-based web application designed to streamline and simplify command line tasks for Ollama users. Our goal is to enhance the user experience by providing a user-friendly interface for managing and interacting with various models and functionalities.

## Core Features

### Up-to-Date Model Access
- **Model Selection**: Easy access to an updated list of models through a user-friendly dropdown menu.

### ModelFile Templater
- **Parameter Customization**: Tailor model parameters like mirostat settings and temperature to your needs.
- **Simplified Deployment**: Deploy models with custom settings, bypassing complex command line processes.

### Detailed Model Insights
- **Model Information**: Access in-depth details about each model, including licensing and parameters.
- **Model Overview**: Quickly view all available models.

### Public Endpoint Management
- **Endpoint Control**: Manage public endpoints for original and OpenAI models with ease.
- **Log Monitoring**: Keep track of endpoint performance through real-time logs.

### LiteLLM Proxy Integration
- **Proxy Management**: Directly control the LiteLLM proxy via a simple interface.
- **Automated Polling**: Effortlessly implement polling for model updates.
- **Log Analysis**: Easily view and analyze LiteLLM proxy logs.
- **Dynamic Configuration**: Maintains a dynamically updated config for all models. Configurations are refreshed and the proxy is rebooted automatically when a new model is detected.

### Additional Utilities
- **CURL Command Creation**: Generate specific CURL commands for model interactions.
- **Manual Model Setup**: Directly create models with custom content and streaming.
- **Log File Handling**: Manage system logs for operational clarity.

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

## Contributing

Contributions to Ollama Companion are highly appreciated. Please refer to our contributing guidelines for submitting pull requests and suggestions.

## License

Ollama Companion is available under [LICENSE]. It is free for use, modification, and distribution under the terms of the license.
