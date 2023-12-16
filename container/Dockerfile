# Use Alpine Linux for a lightweight base image
FROM alpine:latest

# Install git, g++, make, Python, pip, and additional dependencies
RUN apk add --no-cache git g++ make python3 py3-pip \
    python3-dev blas-dev lapack-dev gfortran cmake pkgconfig

# Clone the repository
WORKDIR /usr/src
RUN git clone https://github.com/ggerganov/llama.cpp.git

# Compile the code
WORKDIR /usr/src/llama.cpp
RUN make 

# Set up a Python virtual environment and install dependencies
RUN python3 -m venv /venv
RUN . /venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Add entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the custom script as the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
