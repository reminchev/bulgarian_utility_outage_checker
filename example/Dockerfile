# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and required packages
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        py3-lxml \
    && pip3 install --break-system-packages --no-cache-dir \
        requests \
        beautifulsoup4

# Copy root filesystem
COPY rootfs /

# Make scripts executable
RUN \
    chmod a+x /etc/services.d/example/run \
    && chmod a+x /etc/services.d/example/finish \
    && chmod a+x /usr/bin/outage_checker.py

# Labels
LABEL \
    io.hass.name="Bulgarian Utility Outage Checker" \
    io.hass.description="Check for utility outages in Bulgaria" \
    io.hass.type="addon" \
    io.hass.version="1.1.3"



