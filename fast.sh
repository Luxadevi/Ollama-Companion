#!/bin/bash

# Directory where the modules will be created
MODULES_DIR="./modules"

echo "Creating modules directory..."
mkdir -p $MODULES_DIR

# Function to create a module file
create_module() {
    MODULE_FILE=$MODULES_DIR/$1
    CONTENT=$2
    echo "Creating $MODULE_FILE..."
    echo "$CONTENT" > $MODULE_FILE
}

# High UI module
create_module "high_ui.py" "import gradio as gr

def create_high_ui():
    with gr.Blocks() as high_ui:
        gr.Markdown(\"### High Level Interface\")
        # Add more components for High UI here
    return high_ui"

# Mid UI module
create_module "mid_ui.py" "import gradio as gr

def create_mid_ui():
    with gr.Blocks() as mid_ui:
        gr.Markdown(\"### Mid Level Interface\")
        # Add more components for Mid UI here
    return mid_ui"

# Low UI module
create_module "low_ui.py" "import gradio as gr

def create_low_ui():
    with gr.Blocks() as low_ui:
        gr.Markdown(\"### Low Level Interface\")
        # Add more components for Low UI here
    return low_ui"

# Quant UI module
create_module "quant_ui.py" "import gradio as gr
from high_ui import create_high_ui
from mid_ui import create_mid_ui
from low_ui import create_low_ui

def create_quant_ui():
    high_ui = create_high_ui()
    mid_ui = create_mid_ui()
    low_ui = create_low_ui()

    with gr.Blocks() as quant_ui:
        with gr.Tabs():
            with gr.Tab(\"High\"):
                high_ui()
            with gr.Tab(\"Mid\"):
                mid_ui()
            with gr.Tab(\"Low\"):
                low_ui()
    return quant_ui"

echo "Module files created in $MODULES_DIR"
