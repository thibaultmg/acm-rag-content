FROM quay.io/lightspeed-core/rag-content-cpu:latest

WORKDIR /opt/app-root/src

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

USER root

# Note: The base image uses Python 3.12. We install specific dependencies 
# here rather than the full pyproject.toml to avoid overwriting the pre-compiled 
# data science libraries (like torch) provided by the base image.
RUN uv pip install --system --no-cache-dir pyyaml==6.0.2 llama-index-core==0.14.10

# Ensure the rag user exists (the base image typically provides it as uid 1000)
RUN id -u rag &>/dev/null || useradd -ms /bin/bash rag
USER rag

# Copy the processor script and default config
COPY embedding_generator/custom_processor.py .
COPY embedding_generator/config.yaml .

ENTRYPOINT ["python", "custom_processor.py"]
