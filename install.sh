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

install_packages() {
    # Update package lists
    case "$1" in
        debian)
            sudo apt-get update
            sudo apt-get install -y python3 pip gcc make aria2 build-essential pciutils git # Add 'git' here
            ;;
        redhat)
            sudo yum update
            sudo yum install -y python3 python3-pip gcc make aria2 pciutils git # Add 'git' here
            ;;
        arch)
            sudo pacman -Syu
            sudo pacman -S --noconfirm python3 python-pip gcc make aria2 base-devel pciutils git # Add 'git' here
            ;;
        macos)
            # Assumes Homebrew is installed
            brew update
            brew install python3 pip gcc make aria2 cmake pciutils git # Add 'git' here
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

# Ask macOS and Linux users if they want to install or update Ollama
if [ "$OS" == "macos" ] || [ "$OS" == "debian" ] || [ "$OS" == "redhat" ] || [ "$OS" == "arch" ]; then
    while true; do
        read -p "Do you want to install or update Ollama? (install/update/none): " choice
        case "$choice" in
            install)
                # Install Ollama
                break
                ;;
            update)
                # Update Ollama
                break
                ;;
            none)
                # Do nothing and exit
                echo "No action selected. Exiting..."
                exit 0
                ;;
            *)
                echo "Invalid choice. Please enter 'install', 'update', or 'none'."
                ;;
        esac
    done
fi

# Clone the llama.cpp repository from GitHub
git clone https://github.com/ggerganov/llama.cpp.git

# Linux specific installation for Ollama (if selected)
if [ "$choice" == "install" ] && [ "$OS" == "debian" ] || [ "$OS" == "redhat" ] || [ "$OS" == "arch" ]; then
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
    if [ "$OS" == "jupyter" ]; then
        # Set up Ollama.sh for Jupyter
        echo "Setting up Ollama.sh for Jupyter..."
        if chmod +x /content/ollama.sh && /content/ollama.sh; then
            echo "Ollama.sh setup and executed successfully for Jupyter"
        else
            echo "Failed to set up and execute Ollama.sh for Jupyter" >&2
        fi
    else
        echo "No compatible service management found."
    fi
fi

# Compile llama.cpp if it exists
# Compile llama.cpp if it exists (macOS-specific)
if [ "$OS" == "macos" ] && [ -d "./llama.cpp" ]; then
    cd ./llama.cpp

    # Create a "build" directory if it doesn't exist
    if mkdir -p build; then
        echo "Build directory created successfully"
    else
        echo "Failed to create build directory" >&2
    fi

    # Run CMake from the "build" directory
    if cmake ..; then
        echo "CMake configuration successful"
    else
        echo "CMake configuration failed" >&2
    fi

    # Build the project
    if cmake --build .; then
        echo "Build successful"
    else
        echo "Build failed" >&2
    fi

    # Copy the generated files to the main "llama.cpp" folder
    if cp -r * ..; then
        echo "Generated files copied successfully"
    else
        echo "Failed to copy generated files" >&2
    fi

    # Optional: Clean up the "build" directory (remove it if you don't need it)
    if rm -r build; then
        echo "Build directory removed successfully"
    else
        echo "Failed to remove build directory" >&2
    fi
fi


    # Build the project
    if cmake --build .; then
        echo "Build successful"
    else
        echo "Build failed" >&2
    fi

    # Copy the generated files to the main "llama.cpp" folder
    if cp -r * ..; then
        echo "Generated files copied successfully"
    else
        echo "Failed to copy generated files" >&2
    fi

    # Optional: Clean up the "build" directory (remove it if you don't need it)
    if rm -r build; then
        echo "Build directory removed successfully"
    else
        echo "Failed to remove build directory" >&2
    fi

fi

# Check if Jupyter is detected and build the files in a specific directory
if [ "$OS" == "jupyter" ]; then
    # Assuming /content/Ollama-Companion/llama.cpp is the directory to build in
    if make -C /content/Ollama-Companion/llama.cpp; then
        echo "Build for Jupyter successful"
    else
        echo "Build for Jupyter failed" >&2
    fi
fi

# Check for Linux operating systems and run make
if [ "$OS" != "macos" ] && [ "$OS" != "jupyter" ]; then
    if make -C /llama.cpp; then
        echo "Build for other OS successful"
    else
        echo "Build for other OS failed" >&2
    fi
fi

# Install Python requirements (if requirements.txt exists)
if [ -f requirements.txt ]; then
    if pip install -r requirements.txt; then
        echo "Python requirements installation successful"
    else
        echo "Python requirements installation failed" >&2
    fi
fi
# Run the Python key_generation script
if python3 key_generation.py; then
    echo "Key generation script executed successfully"
else
    echo "Key generation script execution failed" >&2
fi

echo "Installation complete."
echo "Installation complete."
