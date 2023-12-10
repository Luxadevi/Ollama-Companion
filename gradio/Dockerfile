# Use Alpine Linux for a lightweight base image
FROM alpine:latest

# Install git, g++, make, and other necessary tools
RUN apk add --no-cache git g++ make

# Clone the repository
WORKDIR /usr/src
RUN git clone https://github.com/ggerganov/llama.cpp.git

# Compile the code
WORKDIR /usr/src/llama.cpp
RUN make

# Set the entrypoint to the quantize binary
ENTRYPOINT ["./quantize"]
