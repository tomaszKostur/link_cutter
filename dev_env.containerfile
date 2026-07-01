FROM python:3.14-trixie as dev_env
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    bash-completion \
    ca-certificates \
    curl \
    git \
    less \
    locales \
    nano \
    sudo \
    vim \
    zsh \
    tree \
    && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
RUN { \
    echo 'if [ -f /etc/bash_completion ]; then . /etc/bash_completion; fi'; \
    echo 'export HISTFILE=/workspace/.devcontainer/.bash_history'; \
    echo 'alias ll="ls -alF"'; \
    } >> /home/${USERNAME}/.bashrc


USER $USERNAME
WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"