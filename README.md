<h1 align="center">Ollama-Companion</h1>

<p align="center">
  <img src="https://i.imgur.com/ESr6xlT.png" alt="Ollama-Companion Banner" width="600">
</p>




## Enhanced with Streamlit

Ollama-Companion is developed to enhance the interaction and management of Ollama and other large language model (LLM) applications. It aims to support all Ollama API endpoints, facilitate model conversion, and ensure seamless connectivity, even in environments behind NAT. This tool is crafted to construct a versatile and user-friendly LLM software stack, meeting a diverse range of user requirements.

Transitioning from Gradio to Streamlit necessitated the development of new tunneling methods to maintain compatibility with Jupyter Notebooks, like Google Colab.

Explore our Colab Integration to set up the companion within minutes and obtain a public-facing URL.

Interact with Ollama API without typing commands and using a interface to manage your models.
Run Ollama or connect to a client an use this WebUI to manage.
### How to Run

### All-in-one installer ###
 


Clone the repository:


```
git clone https://github.com/Luxadevi/Ollama-Companion.git
```
**Make the linux and mac install script executeable**
```
sudo chmod +x install.sh
```
**Start the linux installer.sh**
```
./install.sh
```

## Starting Ollama-Companion
To start the Companion with a public url for example when you want to share the webpage with others or using this on a service like Colab.
**Use the command.**
```
$ ./start.sh
```
Starting the Companion on a local 127.0.0.1:8501 instance run
```
streamlit run Homepage.py
```

**Note**: Windows support is currently unavailable for running Ollama, but you can run the companion from a Windows client for local quantization and management. You can also manage a remote Ollama instance by setting the Ollama endpoint in the UI.

### Add Your Own Modules
Develop your own Streamlit components and integrate them into Ollama-Companion. See examples using LangChain and other software stacks within Streamlit.
<p align="center">
  <img src="https://i.imgur.com/maRdTU6.png" alt="Ollama-Companion Second Image">
</p>

## LiteLLM Proxy Management

### Overview
This part allows you to manage and interact with the LiteLLM Proxy, which is used to convert over 100 LLM providers to the OpenAI API standard. 

Check LiteLLM out at [LiteLLM proxy ](https://litellm.ai/) 


### LiteLLM Proxy Controls

- **Start LiteLLM Proxy**: Click this button to start the LiteLLM Proxy. The proxy will run in the background and facilitate the conversion process.
- **Read LiteLLM Log**: Use this button to read the LiteLLM Proxy log, which contains relevant information about its operation.
- **Start Polling**: Click to initiate polling. Polling checks for updates to the ollama API and adds any new models to the configuration.
- **Stop Polling**: Use this button to stop polling for updates.
- **Kill Existing LiteLLM Processes**: If there are existing LiteLLM processes running, this button will terminate them.
- **Free Up Port 8000**: Click this button to free up port 8000 if it's currently in use.

*Please note that starting the LiteLLM Proxy and performing other actions may take some time, so be patient and wait for the respective success messages.*

### LiteLLM Proxy Log

The "Log Output" section will display relevant information from the LiteLLM Proxy log, providing insights into its operation and status.

## How to Download Model Files from Hugging Face

To download model files from Hugging Face, follow these steps:

1. **Visit the Model Page**: Go to the Hugging Face model page you wish to download. For example: [Mistralai/Mistral-7B-Instruct-v0.2](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2).

2. **Copy Username/RepositoryName**: On the model page, locate the icon next to the username of the model's author (usually a clipboard or copy symbol). Click to copy the Username/RepositoryName, e.g., `mistralai/Mistral-7B-Instruct-v0.2`.

3. **Paste in the Input Field**: Paste the copied Username/RepositoryName directly into the designated input field in your application.

4. **Get File List**: Click the "Get file list" button to retrieve a list of available files in this repository.

5. **Review File List**: Ensure the list contains the correct model files you wish to download.

6. **Download Model**: Click the "Download Model" button to start the download process for the selected model files.

7. **File Storage**: The model files will be saved in the `llama.cpp/models` directory on your device.

By following these steps, you have successfully downloaded the model files from Hugging Face, and they are now stored in the `llama.cpp/models` directory for your use.


## How to convert Models

## Step One: Model Conversion with High Precision

### Conversion Process

1. **Select a Model Folder**: Choose a folder within `llama.cpp/models` that contains the model you wish to convert.

2. **Set Conversion Options**: Select your desired conversion options from the provided checkboxes, F32 F16 or Q8_0.

3. **Docker Container Option**: Optionally, use a Docker container for added flexibility and compatibility.

4. **Execute Conversion**: Click the "Run Commands" button to start the conversion process.

5. **Output Location**: Converted models will be saved in the `High-Precision-Quantization` subfolder within the selected model folder.

Utilize this process to efficiently convert models while maintaining high precision and compatibility with `llama.cpp`.

## Step Two: Model Quantization Q and Kquants

### Quantization Instructions

1. **Select GGUF File**: Choose the GGUF file you wish to quantize from the dropdown list.

2. **Quantization Options**: Check the boxes next to the quantization options you want to apply (Q, Kquants).

3. **Execution Environment**: Choose to use either the native `llama.cpp` or a Docker container for compatibility.

4. **Run Quantization**: Click the "Run Selected Commands" button to schedule and execute the quantization tasks.

5. **Save Location**: The quantized models will be saved in the `/modelname/Medium-Precision-Quantization` folder.

Follow these steps to perform model quantization using Q and Kquants, saving the quantized models in the specified directory.
Schedule multiple options in a row they will remember and run eventually.

## Model Upload Instructions

Use this section to securely upload your converted models to Hugging Face.

### Steps for Uploading Models

1. **Select a Model**: Choose a model from the dropdown list. These models are located in the `llama.cpp/models` directory.

2. **Enter Repository Name**: Specify a name for the new Hugging Face repository where your model will be uploaded.

3. **Choose Files for Upload**: Select the files you wish to upload from the subfolders of the chosen model.

4. **Add README Content**: Optionally, write content for the README.md file of your new repository.

#### Token Usage
- For enhanced security, use an encrypted token. Encrypt your Hugging Face token on the Token Encrypt page and enter it in the "Enter Encrypted Token" field.
- Alternatively, enter an unencrypted Hugging Face token directly.

5. **Upload Files**: Click the "Upload Selected Files" button to initiate the upload to Hugging Face.

After completing these steps, your uploaded models will be accessible at `https://huggingface.co/your-username/your-repo-name`.

## Try Ollama-Companion
Try ollama Companion deployed on google Colab, with our Colab Notebooks and deploy a instance within minutes. This is available on https://github.com/Luxadevi/Ollama-Colab-Integration




### Core Features

#### Streamlit-Powered Interface
- **Intuitive and Responsive UI**
- **Advanced Modelfile Management**
- **Dynamic UI Building Blocks**

#### Model Compatibility and Conversion
- **Download and Convert PyTorch Models from Huggingface**
- **Multiple Format Conversion Options**

#### Enhanced Connectivity and Sharing
- **Easy API Connectivity via Secure Tunnels**
- **Options for Sharing and Cloud Testing**
- **Accessible from Any Network Setup**

#### Efficient Workflow Management
- **Easy Model Upload to Huggingface**
- **Capability to Queue Multiple Workloads**

#### Security and Configuration
- **Integrated LLAVA Image Analysis**
- **Configurable Security Features**
- **Advanced Token Encryption**

### Future Directions and Contributions

We are dedicated to the continuous enhancement of Ollama-Companion, with a focus on user experience and expanded functionality.


**Check the docs for more information**
### License

Licensed under the Apache License.
