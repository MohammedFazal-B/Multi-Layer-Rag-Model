# Use an NVIDIA CUDA base image to compile llama-cpp-python with GPU support
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# Prevent interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.11, pip, and build tools
RUN apt-get update && apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip cmake build-essential ninja-build && rm -rf /var/lib/apt/lists/*

# Set python3.11 as default python
RUN ln -s /usr/bin/python3.11 /usr/local/bin/python

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Enable CUDA for llama-cpp-python compilation
ENV CMAKE_ARGS="-DGGML_CUDA=on"
ENV FORCE_CMAKE=1

# Install dependencies with a massively increased timeout for large files
RUN for i in 1 2 3 4 5; do pip install --no-cache-dir --default-timeout=2000 -r requirements.txt && break || sleep 3; done

# Install new dependencies separately to preserve the slow llama-cpp-python docker cache
RUN pip install apscheduler

# Copy the rest of the application code
COPY . .

# Command to run your firewall script
CMD ["python", "-m", "src.main"]