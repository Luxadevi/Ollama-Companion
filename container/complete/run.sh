#!/bin/bash

# Function to start the Python application
start_python_app() {
    source venv/bin/activate
    python3.11 run_tunnel .py &
}

# Function to start Streamlit
start_streamlit() {
    source venv/bin/activate
    streamlit run Homepage.py &
}

# Check the passed argument
case "$1" in
    "public" | "-pub")
        # Start Python application for public mode
        start_python_app
        ;;
    "local" | "-lan")
        # Start Streamlit for local mode
        start_streamlit
        ;;
    *)
        echo "Invalid argument. Use 'public' or '-pub' for public mode, 'local' or '-lan' for local mode."
        exit 1
        ;;
esac

# Wait for a short time to ensure the application has started
sleep 5

# Start the Go application in the foreground
exec /bin/ollama serve
