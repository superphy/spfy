#!/usr/bin/bash

echo "Staring production setup..."

# Nginx must be stopped first or Docker can't unbind ports.
if [ "$(grep nginx)" ]; then
    echo "Nginx running. Stopping Nginx...";
    systemctl stop nginx;
    echo "Stopped Nginx.";
else
    echo "Nginx already not running. Continuing...";
fi

# Bring Docker up.
if [ ! "$(docker ps -a | grep webserver)" ]; then
    echo "Docker composition not running. Starting Docker composition...";
    docker-compose up -d;
    echo "Started Docker composition.";
else
    echo "Docker composition already running. Continuing...";
fi

# Bring Nginx up.
echo "Starting Nginx..."
systemctl start nginx
echo "Nginx started."

# Bring Jetty up for Blazegraph.
if [ ! "$(service jetty status | grep pid=)" ]; then
    echo "Jetty not running. Starting Jetty...";
    service jetty start;
    echo "Started Jetty.";
else
    echo "Jetty already running."
fi

echo "Done production setup."