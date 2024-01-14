# First Stage - Building the Go application
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 as builder

ARG TARGETARCH
ARG GOFLAGS="'-ldflags=-w -s'"

WORKDIR /go/src/github.com/jmorganca/ollama

RUN apt-get update && apt-get install -y git build-essential cmake


RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    mkdir llama.cpp/build && \
    cd llama.cpp/build && \
    cmake .. && \
    cmake --build . --config Release

# Second Stage - Setting up Python environment and runtime
FROM ubuntu:22.04

# Install Python 3.11, venv, and other necessary packages
RUN apt-get update && apt-get install -y curl aria2 ca-certificates python3.11 python3.11-venv git

# Clone the Python application repository
WORKDIR /ollama-companion
RUN git clone https://github.com/luxadevi/ollama-companion.git .
RUN git clone https://github.com/ggerganov/llama.cpp.git 
# Set up Python virtual environment and install dependencies
RUN python3.11 -m venv venv
RUN /bin/bash -c "source venv/bin/activate && venv/bin/pip install -r requirements.txt"


# Copy the run.sh script and make it executable
COPY run.sh /run.sh
RUN chmod +x /run.sh

COPY --from=builder /go/src/github.com/jmorganca/ollama/llama.cpp/build/bin /ollama-companion/llama.cpp


EXPOSE 8501
ENV OLLAMA_HOST 0.0.0.0

## Set the entry point to run.sh
ENTRYPOINT ["/run.sh"]
