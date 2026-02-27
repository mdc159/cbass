FROM almir/webhook

USER root
RUN apk add --no-cache bash docker-cli docker-cli-compose

COPY update-container.sh /scripts/update-container.sh
RUN chmod +x /scripts/update-container.sh

# Run as root — this container's sole purpose is executing docker commands
# via the mounted socket, which requires root access
