#!/bin/bash

# Function to check if a command exists in executable paths
is_command_installed() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a specific version of Python is installed
is_python_installed() {
    if is_command_installed python3; then
        local python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        if [[ "$python_version" < "3.10" ]]; then
            echo "Python 3.10 or later is required. Installed version is $python_version."
            return 1
        fi
        echo "Python 3.10 or later is already installed."
        return 0
    else
        echo "Python 3.10 is not installed."
        return 1
    fi
}

# Function to check if Docker is installed
is_docker_installed() {
    is_command_installed docker
}

# Function to install Docker based on OS
install_docker() {
    if is_docker_installed; then
        echo "Docker is already installed."
        return 0
    fi

    case "$1" in
        debian)
            sudo apt-get update && sudo apt-get install -y docker.io
            ;;
        redhat)
            sudo yum update && sudo yum install -y docker
            ;;
        arch)
            sudo pacman -Syu && sudo pacman -S docker
            ;;
        macos)
            brew install docker
            ;;
        *)
            echo "Unsupported OS for Docker installation."
            return 1
            ;;
    esac
    echo "Docker installed successfully."
    return 0
}

<<<<<<< HEAD
# Function to configure Docker
configure_docker() {
    if [ "$1" != "macos" ]; then
        sudo groupadd docker 2>/dev/null || true
        sudo usermod -aG docker $USER
        sudo systemctl start docker
        sudo systemctl enable docker
        echo "Docker configured successfully."
    else
        echo "Docker configuration not required for macOS."
    fi
    return 0
}

# Function to install essential packages
=======
>>>>>>> 6f1ea8e81f5cc1ac6bf4b7bdd2ac629fa3728d8b
install_packages() {
    local packages=("gcc" "make" "aria2" "git")
    local install_needed=false

    for package in "${packages[@]}"; do
        if ! is_command_installed "$package"; then
            install_needed=true
            break
        fi
    done

    if [ "$install_needed" = false ]; then
        echo "All essential packages are already installed."
        return 0
    fi

    case "$1" in
        debian)
<<<<<<< HEAD
            sudo apt-get update && sudo apt-get install -y "${packages[@]}"
            ;;
        redhat)
            sudo yum update && sudo yum install -y "${packages[@]}"
            ;;
        arch)
            sudo pacman -Syu && sudo pacman -S --noconfirm "${packages[@]}"
            ;;
        macos)
            brew install "${packages[@]}"
=======
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
>>>>>>> 6f1ea8e81f5cc1ac6bf4b7bdd2ac629fa3728d8b
            ;;
        *)
            echo "Unsupported OS for package installation."
            return 1
            ;;
    esac
    echo "Packages installed successfully."
    return 0
}
# Function to change ownership and permissions of all files and directories
change_file_ownership() {
    local script_dir="$(dirname "$(realpath "$0")")"
    echo "Changing ownership of all files and directories in $script_dir..."

<<<<<<< HEAD
    # Change ownership to the current user for all files and directories
    find "$script_dir" -exec chown $USER {} \;

    # Change file permissions to read, write, and execute for the owner
    find "$script_dir" -type f -exec chmod u+rwx {} \;
    find "$script_dir" -type d -exec chmod u+rwx {} \;

    echo "Ownership and permissions changed successfully."
}


# Function to determine the operating system
# Function to determine the operating system
detect_os() {
    # Check for Jupyter Notebook environment
    if [ -n "$JUPYTER_RUNTIME_DIR" ]; then
        echo "jupyter"
        return 0
    fi

    local os_name=$(uname -s)
    case "$os_name" in
        Darwin)
            echo "macos"
            ;;
        Linux)
            if grep -qi ubuntu /etc/os-release; then
                echo "debian"
            elif grep -qi centos /etc/os-release; then
                echo "redhat"
            elif grep -qi arch /etc/os-release; then
                echo "arch"
            else
                echo "Unsupported Linux OS."
                return 1
            fi
            ;;
        *)
            echo "Unsupported OS."
            return 1
            ;;
    esac
    return 0
}


# Function to clone the llama.cpp repository
clone_repository() {
    if git clone https://github.com/ggerganov/llama.cpp.git; then
        echo "Repository cloned successfully."
    else
        echo "Failed to clone repository."
        return 1
    fi
    return 0
}

build_llama_cpp() {
    # Check if the OS is Jupyter
    if [ "$1" == "jupyter" ]; then
        # Jupyter Notebook specific build steps
        if [ -d "/content/Ollama-Companion/llama.cpp" ]; then
            if make -C /content/Ollama-Companion/llama.cpp; then
                echo "llama.cpp built successfully in Jupyter Notebook environment."
            else
                echo "Failed to build llama.cpp in Jupyter Notebook environment."
                return 1
            fi
        else
            echo "/content/Ollama-Companion/llama.cpp directory not found."
            return 1
        fi
        return 0
    fi

    # Existing logic for other environments
    if [ -d "llama.cpp" ]; then
        cd llama.cpp

        # Linux: Use make for building
        if [ "$1" == "debian" ] || [ "$1" == "redhat" ] || [ "$1" == "arch" ]; then
            if make; then
                echo "llama.cpp built successfully using make."
            else
                echo "Failed to build llama.cpp using make."
                return 1
            fi
        # macOS: Use CMake for building
        elif [ "$1" == "macos" ]; then
            mkdir -p build && cd build
            cmake .. && cmake --build .
            echo "llama.cpp built successfully using CMake."
            cd ../..
        else
            echo "Unsupported OS for building llama.cpp."
            return 1
        fi
=======
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
>>>>>>> 6f1ea8e81f5cc1ac6bf4b7bdd2ac629fa3728d8b
    else
        echo "llama.cpp directory not found."
        return 1
    fi
    return 0
}
install_python_requirements() {
    local required_packages=("streamlit" "requests" "flask" "flask-cloudflared" "httpx" "litellm" "huggingface_hub" "asyncio" "Pyyaml" "httpx" "APScheduler" "cryptography" "pycloudflared" "numpy==1.24.4" "sentencepiece==0.1.98" "transformers>=4.34.0" "gguf>=0.1.0" "protobuf>=4.21.0" "torch==2.1.1" "transformers==4.35.2")

    for package in "${required_packages[@]}"; do
        if pip install "$package"; then
            echo "$package installed successfully."
        else
            echo "Failed to install $package."
            return 1
        fi
    done

<<<<<<< HEAD
    echo "All required Python packages installed successfully."
    return 0
}

# Function to run the key_generation script
run_key_generation() {
    local script_dir="$1"
    # Change to the script directory to ensure the .key directory is created there
    pushd "$script_dir" > /dev/null
    # Run the key generation script using the full path to avoid any working directory confusion
    if python3 "./key_generation.py"; then
        echo "Key generation script executed successfully."
=======
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
>>>>>>> 6f1ea8e81f5cc1ac6bf4b7bdd2ac629fa3728d8b
    else
        echo "Key generation script execution failed."
        return 1
    fi
    # Return to the previous directory
    popd > /dev/null
    return 0
 }
# Function to prompt for Ollama installation in non-Jupyter environments

# Function to download and run Ollama installer
prompt_ollama_installation() {
    while true; do
        read -p "Do you want to install Ollama? (yes/no): " choice
        case "$choice" in
            yes|YES|y|Y)
                download_and_run_ollama_installer
                break
                ;;
            no|NO|n|N)
                echo "Skipping Ollama installation."
                break
                ;;
            *)
                echo "Please answer yes or no."
                ;;
        esac
    done
}

<<<<<<< HEAD
# Main script execution
create_and_activate_virtualenv() {
    echo "Would you like to create a virtual environment for the Python dependencies? (yes/no)"
    read -r create_venv_choice
    if [[ $create_venv_choice =~ ^[Yy]es$ ]]; then
        echo "Please enter the name for the virtual environment:"
        read -r venv_name
        python3 -m venv "$venv_name"
        # shellcheck disable=SC1090
        source "$venv_name/bin/activate"
        if [ $? -ne 0 ]; then
            echo "Failed to create or activate the virtual environment."
            return 1
        fi
        echo "Virtual environment '$venv_name' created and activated."
    else
        echo "Skipping virtual environment setup."
    fi
    return 0
}
# Function to create a start.sh script
create_start_script() {
    if [ -n "$venv_name" ]; then
        echo "#!/bin/bash" > start.sh
        echo "source $venv_name/bin/activate" >> start.sh
        echo "python3 run_app.py" >> start.sh
        chmod +x start.sh
        echo "start.sh script created. You can run your application using './start.sh'."
    fi
}

# Main script execution
main() {
    local os=$(detect_os)
    local script_dir="$(dirname "$(realpath "$0")")"

    if [ $? -ne 0 ]; then
        echo "Exiting due to unsupported OS."
        exit 1
    fi

    if [ "$os" != "jupyter" ]; then
        if ! is_python_installed; then
            echo "Python 3.10 or later is required but not installed. Exiting."
            exit 1
        fi

        create_and_activate_virtualenv
        if [ $? -ne 0 ]; then
            echo "Failed to set up virtual environment. Exiting."
            exit 1
        fi
        
        # Call create_start_script to create the start.sh file
        create_start_script
    fi

    # Prompt for Ollama installation if not on Jupyter Notebook
    if [ "$os" != "jupyter" ]; then
        prompt_ollama_installation
    fi

    install_docker "$os" && configure_docker "$os"
    install_packages "$os"
    clone_repository
    build_llama_cpp "$os"
    install_python_requirements
    
    # Change file ownership and permissions after all operations
    change_file_ownership

    # Run the key generation script with the correct path
    run_key_generation "$script_dir"

    echo "Installation complete."
}

main
=======
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
>>>>>>> 6f1ea8e81f5cc1ac6bf4b7bdd2ac629fa3728d8b
