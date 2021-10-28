FROM python:3.8

ADD . /neon_email_proxy
WORKDIR /neon_email_proxy
RUN apt-get update && \
    apt-get install -y \
    gcc \
    python3  \
    python3-dev  \
    && pip install wheel  \
    && pip install .

WORKDIR /config

ENV NEON_MQ_PROXY_CONFIG_PATH /config/config.json
ENV NEON_CONFIG_PATH /config
RUN mkdir ~/.config && \
    ln -s /config ~/.config/neon

CMD ["neon_email_proxy"]