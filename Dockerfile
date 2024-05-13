FROM ubuntu:latest
LABEL authors="PC"

# Instalacja podstawowych narzędzi
RUN apt-get update && apt-get install -y \
    git \
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
    libffi-dev \
    libglfw3 \
    libglfw3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libxinerama-dev \
    libxcursor-dev \
    libxi-dev \
    x11-xserver-utils \
    xorg-dev \
    libgl1-mesa-glx


# Instalacja Pythona 3.11.4
RUN curl -O https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tar.xz \
    && tar -xf Python-3.11.4.tar.xz \
    && cd Python-3.11.4 \
    && ./configure --enable-optimizations \
    && make -j 8 \
    && make altinstall

# Instalacja Pythona 3.7.9
RUN curl -O https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tar.xz \
    && tar -xf Python-3.7.9.tar.xz \
    && cd Python-3.7.9 \
    && ./configure --enable-optimizations \
    && make -j 8 \
    && make altinstall

# Instalacja Poetry
RUN curl -sSL https://install.python-poetry.org | python3.11 - --version 1.8.2
ENV PATH="${PATH}:/root/.local/bin"

RUN python3.7 -m pip install numpy pandas laspy pptk

# Pobranie repozytorium i instalacja zależności
ARG GITHUB_TOKEN
RUN git clone https://x-access-token:${GITHUB_TOKEN}@github.com/KTFish/neptuns-eye.git /neptuns-eye \
    && cd /neptuns-eye \
    && git checkout 47-research-how-to-use-docker-in-our-project

WORKDIR /neptuns-eye
RUN poetry env use /usr/local/bin/python3.11
RUN poetry install

# Ustawienie pracy w głównym katalogu aplikacji
WORKDIR /neptuns-eye

COPY USER_AREA.las USER_AREA.las

# Ustawienie pliku main.py jako domyślnego punktu wejścia
ENTRYPOINT ["poetry", "run", "python", "./neptunseye/main.py"]

