#!/bin/sh

# Activate the virtual environment
. /venv/bin/activate

# Check the first argument to the script
case "$1" in
    convert)
        # Run python3 convert.py
        shift  # Remove the first argument
        python3 convert.py "$@"
        ;;
    quantize)
        # Run the quantize binary
        shift  # Remove the first argument
        ./quantize "$@"
        ;;
    *)
        # Default action or an error message
        echo "Invalid argument: $1. Use 'convert' or 'quantize'."
        exit 1
esac
