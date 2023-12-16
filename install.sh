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