FROM quay.io/lightspeed-core/rag-content-cpu@sha256:8e2acc1901b2f07492a3f79391e30ead42cf7139b375e251e74651b98b010af4

WORKDIR /opt/app-root/src

COPY requirements.txt .
USER root
RUN pip install --no-cache-dir -r requirements.txt
USER default

COPY custom_processor.py .
COPY config.yaml .

ENTRYPOINT ["python", "custom_processor.py"]
