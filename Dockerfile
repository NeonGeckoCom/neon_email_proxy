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

ENV NEON_CONFIG_PATH /config

CMD ["neon_email_proxy"]