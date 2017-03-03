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
Description=uWSGI instance to serve spfyapp[Service]
ExecStartPre=-/usr/bin/bash -c 'mkdir -p /run/uwsgi; chown nginx /run/uwsgi'
ExecStart=/usr/bin/bash -c 'cd /opt/backend; source backend activate; uwsgi --ini spfyapp.ini'
[Install] WantedBy=multi-user.target
```
