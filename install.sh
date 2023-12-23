#!/bin/bash
# Install look if user has python env or conda installed
# Adding virtual env options
# Function to check if a command exists in executable paths
is_command_installed() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install pip3
install_pip() {
    local os=$(detect_os)
    case "$os" in
        debian | redhat | arch)
            sudo apt-get update && sudo apt-get install -y python3-pip
            ;;
        macos)
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            python3 get-pip.py --user
            rm get-pip.py
            ;;
        *)
            echo "Unsupported OS for pip installation."
            return 1
            ;;
    esac
    echo "Pip installed successfully."
    return 0
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

    local os=$(detect_os)
    case "$os" in
        debian | redhat | arch)
            sudo apt-get update && sudo apt-get install -y docker.io
            sudo groupadd docker 2>/dev/null || true
            sudo usermod -aG docker $USER
            sudo systemctl start docker
            sudo systemctl enable docker
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

# Function to install essential packages
install_packages() {
    local packages=("gcc" "make" "aria2" "git" "pciutils")
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

    local os=$(detect_os)
    case "$os" in
        debian | redhat | arch)
            sudo apt-get update && sudo apt-get install -y "${packages[@]}"
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

# Function to determine the operating system
detect_os() {
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

# Function to install Python requirements
install_python_requirements() {
    local required_packages=("streamlit" "requests" "flask" "flask-cloudflared" "httpx" "litellm" "huggingface_hub" "asyncio" "PyYAML" "httpx" "APScheduler" "cryptography" "pycloudflared" "numpy==1.24.4" "sentencepiece==0.1.98" "transformers>=4.34.0" "gguf>=0.1.0" "protobuf>=4.21.0" "torch==2.1.1" "transformers==4.35.2")

    for package in "${required_packages[@]}"; do
        if pip3 install "$package"; then
            echo "$package installed successfully."
        else
            echo "Failed to install $package."
            return 1
        fi
    done

    echo "All required Python packages installed successfully."
    return 0
}

# Function to clone and build the llama.cpp repository
clone_and_build_llama_cpp() {
    git clone https://github.com/ggerganov/llama.cpp.git
    if [ ! -d "llama.cpp" ]; then
        echo "Failed to clone llama.cpp."
        return 1
    fi

    local os_name="$(uname -s)"
    case "$os_name" in
        Linux)
            make -C llama.cpp/
            ;;
        Darwin)
            cd llama.cpp/ || return 1
            cmake .
            make
            cd - || return 1
            ;;
        *)
            echo "Unsupported operating system for building llama.cpp."
            return 1
            ;;
    esac

    echo "llama.cpp cloned and built successfully."
    return 0
}

# Function to install Ollama
install_ollama() {
    read -p "Do you want to install Ollama on this host? (y/n) " answer
    case $answer in
        [Yy]* )
            curl https://ollama.ai/install.sh | sh
            echo "Ollama installed on this host."
            ;;
        * )
            echo "Ollama installation skipped."
            ;;
    esac
}

# Function to run the key_generation script
run_key_generation() {
    local script_dir="$(dirname "$(realpath "$0")")"
    pushd "$script_dir" > /dev/null || return 1
    if python3 "./key_generation.py"; then
        echo "Key generation script executed successfully."
    else
        echo "Key generation script execution failed."
        popd > /dev/null || return 1
        return 1
    fi
    popd > /dev/null || return 1
    return 0
}

# Main function
main() {
    local os=$(detect_os)

    if [ "$os" = "Unsupported OS." ]; then
        echo "Exiting due to unsupported OS."
        exit 1
    fi

    if ! is_python_installed; then
        echo "Python 3.10 or later is required but not installed. Exiting."
        exit 1
    fi

    install_pip
    install_docker
    install_packages
    clone_and_build_llama_cpp
    install_python_requirements
    install_ollama
    run_key_generation

    echo "Installation complete."
}

# Call the main function
main
