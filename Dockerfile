FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y lighttpd curl jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/log/lighttpd /etc/lighttpd /var/www \
    && mkdir -p /var/www/cgi-bin /etc/lighttpd/conf.d

COPY lighttpd.conf /etc/lighttpd/
COPY cgi-bin /var/www/cgi-bin

EXPOSE 80
CMD ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
