#!/bin/bash
# Run this script with the arguments -lan or -local to start the companion without
# generating a public URL.

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script's directory
cd "$SCRIPT_DIR"

# Function to kill any existing Python process running `ollama.py`
kill_existing_ollama() {
    pgrep -f 'python3.*ollama\.py' | xargs -r kill -9
    echo "Terminated existing Ollama processes"
}

# Launch virtual environment

start_locally() {
    kill_existing_ollama
    echo "Starting Ollama-Companion locally on port 8501"
    streamlit run Homepage.py
}
start_colab() {
    kill_existing_ollama
    pgrep -f '.*tunnel.*127\.0\.0\.1:8501.*' | xargs -r kill -9
    echo "Starting Ollama-Companion with a public URL"
    python3 run_tunnel.py &
    sleep 8
    python3 "$SCRIPT_DIR/tools/ollama.py" > /dev/null 2>&1 &
    echo "Starting Ollama"
    streamlit run Homepage.py
}

start_public() {
    kill_existing_ollama
    pgrep -f '.*tunnel.*127\.0\.0\.1:8501.*' | xargs -r kill -9
    echo "Starting Ollama-Companion with a public URL"
    python3 run_tunnel.py &
    sleep 8
    streamlit run Homepage.py
}

# Default function to start_public
function_to_run=start_public

# Check if the script is running from `/content/Ollama-Companion` and set `start_colab`
if [[ "$SCRIPT_DIR" == "/content/Ollama-Companion" ]]; then
    function_to_run=start_colab
else
    # Parse arguments to override the default function
    for arg in "$@"; do
        case $arg in
            -local|-lan)
                function_to_run=start_locally
                break
                ;;
            *)
                ;;
        esac
    done
fi

# Run the selected function
$function_to_run
