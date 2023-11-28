#!/bin/bash

# Function to install Python packages
install_python_packages() {
    echo "Installing Python packages..."
    pip install -U gradio requests flask flask-cloudflared httpx litellm PyYAML asyncio
}

# Function to check and install Ollama
install_ollama() {
    if id "ollama" &>/dev/null || getent group "ollama" &>/dev/null; then
        echo "Ollama user or group found, assuming Ollama is installed."
    else
        echo "Installing Ollama..."
        curl -s https://ollama.ai/install.sh | bash
    fi
}

# Function to check Ollama serve port
check_ollama_port() {
    OLLAMA_PORT=$(lsof -i -P -n | grep LISTEN | grep ollama | awk '{print $9}' | cut -d: -f2)
    if [ "$OLLAMA_PORT" == "11434" ]; then
        echo "Ollama serve running on default port, no further action needed."
    else
        echo "Ollama serve is running on a non-default port: $OLLAMA_PORT"
        read -p "Do you want to change the port of the proxy and companion to reflect this? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            change_port_references "$OLLAMA_PORT"
        fi
    fi
}

# Function to change port references in Python scripts
change_port_references() {
    local new_port=$1
    echo "Changing port references to $new_port..."
    sed -i "s/11434/$new_port/g" tools/ollama_companion.py tools/endpoint.py tools/endpointopenai.py

}

# Function to create and enable a systemd service
setup_systemd_service() {
    SERVICE_FILE="/etc/systemd/system/ollama_companion.service"

    echo "Creating systemd service at $SERVICE_FILE"
    cat << EOF | sudo tee $SERVICE_FILE
[Unit]
Description=Ollama Companion Service
After=network.target

[Service]
User=$USER
ExecStart=/usr/bin/python3 /path/to/ollama_companion.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

    echo "Reloading systemd daemon and enabling service..."
    sudo systemctl daemon-reload
    sudo systemctl enable ollama_companion.service
    sudo systemctl start ollama_companion.service
    echo "Ollama Companion service is now enabled and started."
}

# Main script execution
install_python_packages
install_ollama
check_ollama_port

echo "Installation successful! The Ollama companion will now open."
echo "Next time, you can start the companion by running: python3 ./ollama_companion.py"

# Prompt user to set up as a Linux service
read -p "Do you want to set up Ollama Companion as a Linux service? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    setup_systemd_service
fi
