#!/bin/bash
# Run this script with the arguments -lan or -local to start the companion without
# Generating a Public Url.
## Launch virtual environment
source companion_venv/bin/activate
echo "started virtual env"

start_locally() {
    echo "starting Ollama-Companion locally on port 8501"
    streamlit run Homepage.py
}

start_public() {
    pgrep -f '.*tunnel.*127\.0\.0\.1:8501.*' | xargs -r kill -9
    echo "starting Ollama-Companion with a public URL"
    python3 run_tunnel.py &
    sleep 3
    streamlit run Homepage.py
}

# Default function to start_public
function_to_run=start_public

# Parse arguments
for arg in "$@"
do
    case $arg in
        -local|-lan)
            function_to_run=start_locally
            break
            ;;
        *)
            ;;
    esac
done

# Run the selected function
$function_to_run
