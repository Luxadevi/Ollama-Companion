#!/bin/bash
# this is the Ollama-Companion bash installer for Linux 
# This installer is meant to be ran from a direct download or from the ollama-companion repo



# These packages are needed to install or use ollama/companion.
COMMON_PACKAGES="aria2 make gcc git pciutils curl" # Replace with actual package names

# Function to install packages
install_packages() {
    if [[ "$1" == "Ubuntu" || "$1" == "Debian" ]]; then
        sudo apt update
        sudo apt install -y $COMMON_PACKAGES
    elif [[ "$1" == "Arch" ]]; then
        sudo pacman -Syu
        sudo pacman -S $COMMON_PACKAGES
    elif [[ "$1" == "RedHat" ]]; then
        sudo yum update
        sudo yum install -y $COMMON_PACKAGES
    fi
}

# Function to check Python 3.10 and python3.10-venv
check_python() {
    PYTHON_VERSION=$(python3 --version 2>/dev/null | grep -oP '(?<=Python )\d+\.\d+')
    PYTHON_VENV_PACKAGE="python3.10-venv" 

    if [[ $PYTHON_VERSION < 3.10 ]]; then
        echo "Python 3.10 or higher is not installed. Please install it using your distribution's package manager."
        case $1 in
            "Ubuntu"|"Debian")
                echo "Run: sudo apt install python3.10 python3.10-venv (or higher)" 
                ;;
            "Arch")
                echo "Run: sudo pacman -S python3.10 python3.10-venv (or higher)"  Adjust if package names differ
                ;;
            "RedHat")
                echo "Run: sudo yum install python3.10 python3.10-venv (or higher)" # Adjust if package names differ
                ;;
            *)
                echo "Unsupported distribution."
                ;;
        esac
    else
        echo "Python 3.10 or higher is installed."
    fi
}

# Function to create a Python virtual environment
create_python_venv() {
    if command -v python3.10 >/dev/null 2>&1; then
        python3.10 -m venv companion_venv
        echo "Virtual environment created with Python 3.10 in 'companion_venv' directory."
    elif command -v python3.11 >/dev/null 2>&1; then
        python3.11 -m venv companion_venv
        echo "Virtual environment created with Python 3.11 in 'companion_venv' directory."
    elif command -v python3 >/dev/null 2>&1; then
        python3 -m venv companion_venv
        echo "Virtual environment created with default Python 3 in 'companion_venv' directory."
    else
        echo "No suitable Python 3 version found. Please install Python 3."
        return 1
    fi
}


# Function to activate the virtual environment
activate_venv() {
    source companion_venv/bin/activate
    echo "Virtual environment activated."
}

# Function to install dependencies from requirements.txt
pip_dependencies() {
    pip install -r requirements.txt
    echo "Dependencies installed from requirements.txt."
}


# Detect the OS
OS="Unknown"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
fi


# Function to clone ollama-companion repository
clone_ollama_companion() {
    current_dir=$(basename "$PWD")
    if [ "$current_dir" != "ollama-companion" ]; then
        git clone https://github.com/luxadevi/ollama-companion.git
        cd ollama-companion
        echo "Cloned ollama-companion and changed directory to ollama-companion"
    else
        echo "Already inside ollama-companion directory, skipping clone."
    fi
}

# Function to clone llama.cpp repository and run make in its directory
clone_and_make_llama_cpp() {
    git clone https://github.com/ggerganov/llama.cpp.git
    make -C llama.cpp
    echo "Cloned llama.cpp and ran make in the llama.cpp directory"
}

# Interactive options
# Function to install Ollama
install_ollama() {
    read -p "Do you want to install Ollama on this computer? (y/n) " answer
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

clean_build_llama_cpp() {
    echo "Do you want to clean build llama.cpp? (yes/no)"
    read clean_build_response
    if [[ $clean_build_response == "yes" ]]; then
	git clone http://github.com/ggerganov/llama.cpp.git
        make -C llama.cpp
        echo "Clean build of llama.cpp completed."
    else
        echo "Skipping clean build of llama.cpp."
    fi
}

interactive_check_python() {
    PYTHON_VERSION=$(python3 --version 2>/dev/null | grep -oP '(?<=Python )\d+\.\d+')
    if [[ $PYTHON_VERSION < 3.10 ]]; then
        echo "Python 3.10 or 3.11 is required. Would you like to install it? (yes/no)"
        read install_python
        if [[ $install_python == "yes" ]]; then
            case $OS in
                "Ubuntu"|"Debian")
                    sudo apt install -y python3.10 python3.10-venv || sudo apt install -y python3.11 python3.11-venv
                    ;;
                "Arch")
                    sudo pacman -S python3.10 python3.10-venv || sudo pacman -S python3.11 python3.11-venv
                    ;;
                "RedHat")
                    sudo yum install -y python3.10 python3.10-venv || sudo yum install -y python3.11 python3.11-venv
                    ;;
                *)
                    echo "Unsupported distribution for automatic Python installation."
                    ;;
            esac
        fi
    else
        echo "Python 3.10 or higher is already installed."
    fi
}

# END message when the installation is completed

END_MESSAGE="Ollama successfully installed, you can launch next time with the start.sh script. Ollama-companion will autolaunch on port 8051 and defaults to making a public facing url for your companion. If you only want to run Ollama-companion locally: run the start.sh script with '-local' or '-lan' arguments."


## Installation-types
# There are 4 different types of installations
# Use the arguments -minimal -min, -large -l, or use -interactive or -i to install the client interactively.
# Otherwise the installation will do a standard installation without pytorch and ollama.
# Minimal installation function
install_minimal() {
    echo "Starting minimal installation..."
    install_packages "$OS"
    check_python "$OS"
    clone_ollama_companion
    create_python_venv
    activate_venv
    pip_dependencies
    echo "$END_MESSAGE" 
}

# Medium installation function
install_medium() {
    echo "Starting Standard installation..."
    install_packages "$OS"
    check_python "$OS"
    clone_ollama_companion
    clone_and_make_llama_cpp
    create_python_venv
    activate_venv
    pip_dependencies
    echo "$END_MESSAGE" 
}

# Large installation function
install_large() {
    echo "Starting Complete installation..."
    install_packages "$OS"
    check_python "$OS"
    clone_ollama_companion
    clone_and_make_llama_cpp
    create_python_venv
    activate_venv
    pip_dependencies
    pip install torch 
    install_ollama
    echo "$END_MESSAGE"
}

# Interactive installation function
install_interactive() {
    echo "Starting interactive installation..."
    install_ollama
    interactive_check_python
    echo "Cloning Ollama-companion directory"
    clone_ollama_companion
    clean_build_llama_cpp
    echo "Do you want to use the included virtual environment and install all Python dependencies ? (recommended) (yes/no)"
    read use_venv_response
    if [[ $use_venv_response == "yes" ]]; then
        create_python_venv
        activate_venv
        pip_dependencies
        pip install torch
        echo "Virtual environment set up and dependencies installed."
    else
        echo "Skipping virtual environment setup and Python dependency installation."
	echo "Install the needed python dependencies from the requirements.txt with pip install -r requirements.txt"
	echo "Recommended to install these python libraries in a virtual enviroment"
    fi
    echo "$END_MESSAGE"
}

# Main execution logic
main() {
    # Detect the OS
    OS="Unknown"
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
    fi

    case $1 in
        -minimal|-min)
            install_minimal
            ;;
        -large|-l)
            install_large
            ;;
        -interactive|-i)
            install_interactive
            ;;
        *)
            install_medium
            ;;
    esac
}

# Call the main function with all passed arguments
main "$@"
