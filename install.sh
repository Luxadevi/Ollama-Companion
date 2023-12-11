#!/bin/bash

# Function to install and configure Docker
install_and_configure_docker() {
    case "$1" in
        debian | redhat | arch)
            # Install Docker
            sudo apt-get install -y docker.io

            # Configure Docker
            sudo groupadd docker
            sudo gpasswd -a $USER docker
            sudo usermod -aG docker $USER
            sudo chown root:docker /var/run/docker.sock
            sudo chown -R root:docker /var/run/docker
            ;;
        macos)
            # Assumes Homebrew is installed
            brew install docker
            ;;
        *)
            echo "Docker installation not supported on this OS"
            exit 1
            ;;
    esac
}

# Function to install packages
install_packages() {
    # Update package lists
    case "$1" in
        debian)
            sudo apt-get update
            sudo apt-get install -y python3 pip gcc make aria2 build-essential pciutils
            ;;
        redhat)
            sudo yum update
            sudo yum install -y python3 python3-pip gcc make aria2 pciutils
            ;;
        arch)
            sudo pacman -Syu
            sudo pacman -S --noconfirm python3 python-pip gcc make aria2 base-devel pciutils
            ;;
        macos)
            # Assumes Homebrew is installed
            brew update
            brew install python3 pip gcc make aria2 cmake pciutils
            ;;
        *)
            echo "Unsupported OS"
            exit 1
            ;;
    esac
}

# Detect OS
OS="unknown"
if [ "$(uname)" == "Darwin" ]; then
    OS="macos"
elif [ -f /etc/debian_version ]; then
    OS="debian"
elif [ -f /etc/redhat-release ]; then
    OS="redhat"
elif [ -f /etc/arch-release ]; then
    OS="arch"
elif grep -q Microsoft /proc/version 2>/dev/null; then
    echo "WOW, you ran a bash script inside Windows. Sadly, Windows is not supported with Ollama but you can still use this web UI to interface with an Ollama endpoint and use the quantize functions."
    ./window_install.ps1
    exit 0
fi

# Install packages
install_packages $OS

# Install and configure Docker
install_and_configure_docker $OS

# macOS specific installation for Ollama
if [ "$OS" == "macos" ]; then
    echo "Downloading Ollama for macOS..."
    mkdir -p /MacOS
    curl -o /MacOS/Ollama-darwin.zip https://ollama.ai/download/Ollama-darwin.zip
    unzip /MacOS/Ollama-darwin.zip -d /MacOS/
fi

# Linux specific installation for Ollama
if [ "$OS" == "debian" ] || [ "$OS" == "redhat" ] || [ "$OS" == "arch" ]; then
    curl -O https://ollama.ai/install.sh
    chmod +x install.sh
    ./install.sh
fi

# Systemd setup for Linux
if [ "$OS" != "macos" ] && systemctl | grep -q '\-\.mount'; then
    echo "Adding systemd configuration for Ollama..."
    mkdir -p /etc/systemd/system/ollama.service.d
    echo '[Service]' >> /etc/systemd/system/ollama.service.d/environment.conf
    echo 'Environment="OLLAMA_HOST=0.0.0.0:11434"' >> /etc/systemd/system/ollama.service.d/environment.conf

    echo "Reloading systemd and restarting Ollama..."
    sudo systemctl daemon-reload
    sudo systemctl restart ollama
fi

# Launchd setup for macOS
if [ "$OS" == "macos" ]; then
    if command -v launchctl >/dev/null 2>&1; then
        echo "Adding launchd configuration for Ollama..."

        # Create a plist file for your service
        cat <<EOF > /Library/LaunchDaemons/com.yourcompany.ollama.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.yourcompany.ollama</string>
    <key>ProgramArguments</key>
    <array>
        <string>/MacOS/Ollama.app/Contents/MacOS/Ollama</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_HOST</key>
        <string>0.0.0.0:11434</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

        # Load the launchd configuration
        launchctl load /Library/LaunchDaemons/com.yourcompany.ollama.plist

        echo "Starting Ollama..."
    else
        echo "launchctl not found. Unable to create launchd configuration."
    fi
fi

else
    # Check for Jupyter
    if [ -n "$JUPYTERHUB_SERVICE_PREFIX" ]; then
        echo "Jupyter notebook detected. Start Ollama from the web interface."
    else
        echo "No compatible service management found."
    fi
fi

# Compile llama.cpp if exists
if [ -d "./llama.cpp" ]; then
    cd ./llama.cpp
    if [ "$OS" == "macos" ]; then
        cmake .
    else
        make
    fi
    cd ..
    else ./llama.cpp make
fi

# Install Python requirements
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "Installation complete."




