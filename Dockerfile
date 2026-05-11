FROM python:3.12-bookworm
SHELL ["/bin/bash", "-c"]
# Replace the placeholder <origin2target>
WORKDIR /home/swing2angular-poc

RUN apt update && \
    apt install -y zip curl gnupg && \
    curl -s "https://get.sdkman.io" | bash && \
    source "/root/.sdkman/bin/sdkman-init.sh" && \
    curl -sL https://deb.nodesource.com/setup_22.x | bash - && \
    apt update && \
    apt install -y nodejs && \
    npm install @openapitools/openapi-generator-cli -g && \
    sdk install java 21.0.2-open

# Create a virtual environment
ENV VIRTUAL_ENV=venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Add Tini to avoid zombie processes
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /tini
COPY pyproject.toml pyproject.toml
COPY --from=genrevive . /home/genrevive
RUN python3 -m venv $VIRTUAL_ENV && \
    pip install poetry==1.8.3 && \
    poetry lock && \
    poetry install && \
    chmod +x /tini
ENV PATH=/root/.sdkman/candidates/java/current/bin:$PATH
COPY .env .env
RUN sed -i 's/\r$//' .env  && \
    # Replace placeholder <TARGET_PROJECT_PATH>
    source .env && \
    mkdir -p $TARGET_PROJECT_PATH  && \
    # No longer needed for image build; Environment variables will be pass to the running container
    rm .env

COPY . .

ENTRYPOINT ["/tini", "--"]
CMD ["/bin/bash", "-c", "python3 main.py"]
