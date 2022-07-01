FROM python:3.9.7 as base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app


FROM base as poetry
RUN pip install poetry==1.1.13
COPY poetry.lock pyproject.toml /app/
RUN poetry export -o requirements.txt


FROM python:3.9.7-slim as runtime
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update --fix-missing

RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    openssl \
    graphviz \
    pkg-config \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y  $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    libgraphviz-dev \
    python-dev \
    " \
    && apt-get update && apt-get install -y  $BUILD_DEPS

WORKDIR /app

COPY ./src /app

COPY --from=poetry /app/requirements.txt /tmp/requirements.txt
RUN pip install 'wheel==0.37.1' && pip install -r /tmp/requirements.txt

ENV PYTHONUNBUFFERED 1

RUN ls -la

CMD [ "python", "manage.py", "makemigrations", "&&", "python", "manage.py", "migrate"]