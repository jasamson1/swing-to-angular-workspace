FROM python:3.12-bookworm
SHELL ["/bin/bash", "-c"]

WORKDIR /home/swing2angular-poc

#Install Poetry globally in the system python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==1.8.5

RUN echo "virtualenv<20.26.6" > /tmp/constraints.txt
ENV PIP_CONSTRAINT=/tmp/constraints.txt

COPY --from=genrevive . /home/genrevive
COPY pyproject.toml .

RUN pip install langdetect
RUN poetry install --no-interaction --no-ansi

#Configure poetry to install directly into the system (no venv needed in Docker)
RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi

RUN apt update && \
    apt install -y zip curl gnupg && \
    curl -s "https://get.sdkman.io" | bash && \
    source "/root/.sdkman/bin/sdkman-init.sh" && \
    curl -sL https://deb.nodesource.com/setup_22.x | bash - && \
    apt update && \
    apt install -y nodejs && \
    npm install @openapitools/openapi-generator-cli -g && \
    sdk install java 21.0.2-open

ENV PATH=/root/.sdkman/candidates/java/current/bin:$PATH

COPY . .

# Add Tini to avoid zombie processes
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /tini
RUN chmod +x /tini

ENTRYPOINT ["/tini", "--"]
CMD ["/bin/bash", "-c", "python3 main.py"]
