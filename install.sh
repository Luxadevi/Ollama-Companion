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

    # Enable automatic start on boot
    sudo systemctl enable ollama_companion.service
}

# Function to ask the user if they want to install Ollama on this host or a different address
ask_install_location() {
    read -p "Do you want to install Ollama on this host (y/n)? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_ollama
    else
        echo "You have chosen not to install Ollama on this host. Please install it manually on your desired address."
    fi
}

# Function to ask the user if they want to set up Ollama Companion as a systemd service
ask_setup_systemd_service() {
    read -p "Do you want to set up Ollama Companion as a systemd service (recommended)? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_systemd_service
    fi
}

# Main script execution
install_python_packages

# Ask the user where they want to install Ollama
ask_install_location

echo "Installation successful! The Ollama Companion will now open."

# Ask the user if they want to set up Ollama Companion as a systemd service
ask_setup_systemd_service

# Check if Ollama Companion was set up as a system process
if [ -f /etc/systemd/system/ollama_companion.service ]; then
    echo "Ollama Companion has been set up as a system process and will start automatically on boot."
else
    echo "Ollama Companion started. If you didn't make this a system process, start the app next time with 'python3 main.py' in this directory."
fi

# Start python3 main.py once the script is done
python3 main.py
