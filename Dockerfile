FROM python:3.7-alpine
WORKDIR /
COPY . /
RUN true && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev make && \
    make setup dist && \
    apk del --no-cache .build-deps

FROM python:3.7-alpine
LABEL maintainer="Wazo Authors <dev@wazo.community>"
ENV VERSION 1.0.0
COPY --from=0 /dist/wazo_router_confd-1.0-py3-none-any.whl /tmp/wazo_router_confd-1.0-py3-none-any.whl
RUN true && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev make && \
    pip install --no-cache-dir /tmp/wazo_router_confd-1.0-py3-none-any.whl && \
    apk del --no-cache .build-deps && \
    rm /tmp/wazo_router_confd-1.0-py3-none-any.whl && \
    apk add netcat-openbsd

COPY ./scripts/wait-for /usr/bin/wait-for
RUN chmod +x /usr/bin/wait-for
