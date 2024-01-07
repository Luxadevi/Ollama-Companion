# First Stage - Building the Go application
FROM nvidia/cuda:11.8.0-devel-ubuntu22.04 as builder

ARG TARGETARCH
ARG GOFLAGS="'-ldflags=-w -s'"

WORKDIR /go/src/github.com/jmorganca/ollama

RUN apt-get update && apt-get install -y git build-essential cmake
ADD https://dl.google.com/go/go1.21.3.linux-$TARGETARCH.tar.gz /tmp/go1.21.3.tar.gz
RUN mkdir -p /usr/local && tar xz -C /usr/local </tmp/go1.21.3.tar.gz

COPY . .
ENV GOARCH=$TARGETARCH
ENV GOFLAGS=$GOFLAGS
RUN /usr/local/go/bin/go generate ./... \
    && /usr/local/go/bin/go build .

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

# Copy the built Go application from the first stage
COPY --from=builder /go/src/github.com/jmorganca/ollama/ollama /bin/ollama

# Copy the run.sh script and make it executable
COPY run.sh /run.sh
RUN chmod +x /run.sh

COPY --from=builder /go/src/github.com/jmorganca/ollama/llama.cpp/build/bin /ollama-companion/llama.cpp


EXPOSE 11434
ENV OLLAMA_HOST 0.0.0.0

# Set environment variables for NVIDIA compatibility
ENV PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Set the entry point to run.sh
ENTRYPOINT ["/run.sh"]
