`cd ~/backend`

# Blazegraph
`bash superphy/database/scripts/start.sh`

# Redis
```
Since Redis 2.6 it is possible to pass Redis configuration parameters using the command line directly. This is very useful for testing purposes.

redis-server --daemonize yes
Check if the process started or not:

ps aux | grep redis-server
```

# uWSGI & Nginx on Cent
[How to Serve Python Apps using uWSGI and Nginx on Centos-7](https://hostpresto.com/community/tutorials/how-to-serve-python-apps-using-uwsgi-and-nginx-on-centos-7/)

`sudo vim /etc/systemd/system/uwsgi.service`

add

```
[Unit]
Description=uWSGI Emperor service
After=network.target

[Service]
ExecStartPre=/usr/bin/bash -c 'source /opt/miniconda2/envs/backend/bin/activate backend; mkdir -p /run/uwsgi; chown spfy:deployments /run/uwsgi; export PYTHONPATH=/opt/miniconda2/envs/backend/bin/python; export PATH=/opt/miniconda2/envs/backend/bin; which python; which rgi; echo $PATH; export PYTHONHOME=/opt/miniconda2/envs/backend/bin/python'
ExecStart=/usr/bin/bash -c 'source /opt/miniconda2/envs/backend/bin/activate backend; export PYTHONPATH=/opt/miniconda2/envs/backend/bin/python; export PATH=/opt/miniconda2/envs/backend/bin; /opt/miniconda2/bin/uwsgi --ini /opt/backend/spfyapp.ini'
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

Now, you can start the service by running:
`sudo systemctl start uwsgi`

To check the status of service, run:
`sudo systemctl status uwsgi`

nginx.conf
```
# from /etc/nginx/nginx.conf
user spfy;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /opt/backend/app;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location / {
	         include uwsgi_params;
           uwsgi_pass unix:/run/uwsgi/backend.sock;
        }

        location /static {
          alias /opt/backend/app/static;
        }
    }
}
```
