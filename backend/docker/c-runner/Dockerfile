FROM gcc:12

RUN useradd -m runner || true
USER runner
WORKDIR /work
ENTRYPOINT ["/bin/sh", "-c"]
