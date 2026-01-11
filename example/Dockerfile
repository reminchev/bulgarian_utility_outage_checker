# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and required packages from Alpine repos
RUN apk add --no-cache \
    python3 \
    py3-requests \
    py3-beautifulsoup4 \
    py3-lxml

# Copy root filesystem
COPY rootfs /

# Make scripts executable
RUN chmod a+x /etc/services.d/example/run && \
    chmod a+x /etc/services.d/example/finish && \
    chmod a+x /usr/bin/outage_checker.py

# Labels
LABEL \
    io.hass.name="Bulgarian Utility Outage Checker" \
    io.hass.description="Check for utility outages in Bulgaria" \
    io.hass.type="addon" \
    io.hass.version="1.1.4"




