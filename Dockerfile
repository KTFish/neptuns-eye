FROM ubuntu:latest
LABEL authors="PC"

ENTRYPOINT ["top", "-b"]

FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev

RUN curl -O https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tar.xz \
    && tar -xf Python-3.11.0.tar.xz \
    && cd Python-3.11.0 \
    && ./configure --enable-optimizations \
    && make -j 8 \
    && make altinstall

# Instalacja curl i Poetry
RUN apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3.11 - --version 1.8.2

# Dodanie .local/bin do PATH
ENV PATH="${PATH}:/root/.local/bin"

# Sprawdzenie wersji Poetry
RUN poetry --version
