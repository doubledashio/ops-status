FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /

RUN apt-get update && \
    apt-get install -y  --no-install-recommends \
    file \
    gcc \
    g++ \
    wget && \
    pip install --upgrade --no-cache-dir \
    pip \
    setuptools && \
    pip install --no-cache-dir \
    -r /requirements.txt && \
    rm -rf /tmp/* /var/lib/apt/lists/* /var/cache/apt/* && \
    apt-get purge -y --auto-remove gcc g++

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN useradd -ms /bin/bash app

USER app

COPY --chown=app:app . /home/app/

WORKDIR /home/app/ops_status

CMD ["/home/app/.docker/web.sh"]
