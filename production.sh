#!/usr/bin/bash

echo "Staring production setup..."

# Nginx must be stopped first or Docker can't unbind ports.
if pgrep -x "gedit" > /dev/null; then
    echo "Nginx running. Stopping Nginx...";
    systemctl stop nginx;
    echo "Stopped Nginx.";
else
    echo "Nginx already not running. Continuing...";
fi

# Bring Docker up.
if [ ! "$(docker ps -a | grep webserver)" ]; then
    echo "Docker composition not running. Starting Docker composition...";
    cd /opt/spfy && docker-compose up -d;
    echo "Started Docker composition.";
else
    echo "Docker composition already running. Continuing...";
fi

# Bring Nginx up.
echo "Starting Nginx..."
systemctl start nginx
echo "Nginx started."

# Bring Jetty up for Blazegraph.
if pgrep -x "gedit" > /dev/null; then
    echo "Jetty not running. Starting Jetty...";
    service jetty start;
    echo "Started Jetty.";
else
    echo "Jetty already running."
fi

echo "Done production setup."
