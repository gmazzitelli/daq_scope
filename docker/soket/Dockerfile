FROM alpine:latest

RUN apk --update add --no-cache openssh
RUN apk add bash && rm -rf /var/cache/apk/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# COPY ./spaip_rsa /root/.ssh/id_rsa
# RUN chmod 600 /root/.ssh/id_rsa

ENTRYPOINT ["/entrypoint.sh"]
