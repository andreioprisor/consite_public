FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Set environment variable to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create Python symlink after installation
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Set the working directory
WORKDIR /app

# Set CUDA environment variables
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# Copy and install requirements first (better layer caching)
COPY reqs.txt llm_reqs.txt ./

# Install requirements with specific cuda configuration for bitsandbytes
RUN pip3 install --no-cache-dir -r reqs.txt && \
    pip3 install --no-cache-dir -r llm_reqs.txt && \
    pip3 install --no-cache-dir --upgrade torch --index-url https://download.pytorch.org/whl/cu121 && \
    pip3 install --no-cache-dir bitsandbytes --upgrade

# Copy the rest of the application
COPY . .

EXPOSE 65432

# Use explicit python3 in CMD
CMD ["python3", "endpoint.py"]