FROM python:3.11-slim

RUN useradd -m runner || true
USER runner
WORKDIR /work
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["/bin/sh", "-c"]
