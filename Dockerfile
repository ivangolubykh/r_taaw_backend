FROM python:3.13
ARG USERNAME=python_my
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV PIP_NO_CACHE_DIR=on
RUN apt update && \
    apt install -y --no-install-recommends net-tools locales gettext && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen; \
    locale-gen && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --upgrade pip && \
    groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:ru
ENV LC_ALL en_US.UTF-8

USER $USERNAME
WORKDIR /home/$USERNAME/django_app

RUN pip3 install pipenv
ENV PATH=$PATH:/home/$USERNAME/.local/bin

COPY --chown=$USERNAME:$USER_GID Pipfile Pipfile
COPY --chown=$USERNAME:$USER_GID Pipfile.lock Pipfile.lock
RUN pipenv install --system --deploy --ignore-pipfile
