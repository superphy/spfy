`cd /opt`

`sudo groupadd deployments`
`sudo useradd spfy`
`sudo usermod -aG deployments spfy`
`sudo passwd spfy`
`su - spfy`

`git clonehttps://github.com/superphy/backend.git`

`cd backend/`

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

[Service]
ExecStartPre=/usr/bin/bash -c 'source /opt/miniconda2/envs/backend/bin/activate backend; mkdir -p /run/uwsgi; chown spfy:deployments /run/uwsgi; export PYTHONPATH=/opt/miniconda2/envs/backend/bin/python; export PATH=/opt/miniconda2/envs/backend/bin; which python; which rgi; echo $PATH; export PYTHONHOME=/opt/miniconda2/envs/backend/bin/python'
ExecStart=/usr/bin/bash -c 'source /opt/miniconda2/envs/backend/bin/activate backend; export PYTHONPATH=/opt/miniconda2/envs/backend/bin/python; export PATH=/opt/miniconda2/envs/backend/bin; /opt/miniconda2/bin/uwsgi --emperor /opt/backend/uwsgi'
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

from /etc/nginx/nginx.conf
```
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

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

    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    server {
	client_max_body_size 200m;
	listen       80 default_server;
	listen       443 ssl http2 default_server;
        listen       [::]:80 default_server;
	listen       [::]:443 ssl http2 default_server;
	server_name  superphy.corefacility.ca;
        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;


	location / {
            proxy_pass http://127.0.0.1:8081;
	}
	location /spfy/ {
	    rewrite ^/spfy/(.*)$ /$1 break;
      	    proxy_pass http://localhost:8080;
      	    proxy_redirect http://localhost:8080/ $scheme://$host/spfy/;
     	    proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
      	    proxy_set_header Connection $connection_upgrade;
      	    proxy_read_timeout 20d;
	}
	location /shiny/ {
	    proxy_pass http://127.0.0.1:3840;
	}

    }

    server {
        client_max_body_size 200m;
        listen       80;
        listen       443 ssl http2;
        listen       [::]:80;
        listen       [::]:443 ssl http2;
        server_name  lfz.corefacility.ca;
        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

	location / {
            proxy_pass http://127.0.0.1:8081;
	}
	location = /spfy {
	    return 301 /superphy/spfy/;
	}
	location /spfy/ {
            rewrite ^/spfy/(.*)$ /$1 break;
            proxy_pass http://localhost:8080;
            proxy_redirect http://localhost:8080/superphy/ $scheme://$host/spfy/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_read_timeout 20d;
        }
	location /shiny/ {
	    proxy_pass http://127.0.0.1:3840;
	}
    }


}
```

perms for nginx uploads
`sudo chown -R spfy:deployments /var/lib/nginx/`


```
[Unit]
Description=Single RQ Worker service

[Service]
ExecStartPre=/usr/bin/bash -c 'source /opt/miniconda2/envs/backend/bin/activate backend; export PYTHONPATH=/opt/miniconda2/envs/backend/bin/python; export PATH=/opt/miniconda2/envs/backend/bin; export PYTHONHOME=/opt/miniconda2/envs/backend/bin/python'
ExecStart=/usr/bin/bash -c 'source /opt/miniconda2/envs/backend/bin/activate backend; export PYTHONPATH=/opt/miniconda2/envs/backend/bin/python; export PATH=/opt/miniconda2/envs/backend/bin; nohup rq worker high low &'
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

if you need to debug
`rq dashboard`

open port: (this is specific to Cent7)
* check which zone you're in `firewall-cmd --get-active-zones`
* add the port (note the zone here was `public`) `firewall-cmd --zone=public --add-port=9181/tcp --permanent`
* reload the firewall `sudo firewall-cmd --reload`
