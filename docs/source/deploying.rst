================
Deplyoment Guide
================

.. contents:: Table of Contents
   :local:
   
The way we recommend you deploy Spfy is to simply use the Docker composition for everything; this approach is documented in `Deploying in General`_. Specifics related to the NML's deployment is given in `Deploying to Corefacility`_.
   
Deploying in General
====================

Most comments are based of the ``docker-compose.yml`` file at the project root.

	    
Host to Container Mapping
-------------------------
	    
There are a few key points to note:

.. code-block:: yaml

	ports:
	- "8000:80"
	
The configuration maps ``host:container``; so port 8000 on the host (your computer) is linked to port 80 of the container. Fields like volumes typically have only one value: ``/var/lib/jetty/``; this is done to instruct Docker to map the folder ``/var/lib/jetty`` within the container itself to a generic volume managed by Docker, thereby enabling the data to persist across start/stop cycles.

You can also add a host path to volume mappings such as ``/dbbackup/:/var/lib/jetty/`` so that Docker uses an actual path on your host, instead of a generic Docker-managed volume. As before, the first term, ``/dbbackup/`` would reside on the host.

.. warning::

	Generally, you should stop a Docker composition by running ``docker-compose stop`` instead of ``docker-compose down``. As of the most recent Docker versions, a ``docker-compose down`` should not remove the Docker volumes, but this has been inconsistent in the past.

Volume Mapping in Production
----------------------------

In production, at minimum we recommend you map Blazegraph's volume to a backup directory. ``/datastore`` also stores all the uploaded genome files and related temporary files generated during analysis.

Ports
-----

``grouch`` is the front-end user interface for Spfy whereas ``webserver`` serves the backend Flask APIs. Without modification, when you run ``docker-compose up`` port 8090 is used to access the app. The front-end then calls port 8000 to submit requests to the backend. This approach is fine for individual users on their own computer, but this setup should not be used for production as it would you would have to open a separate port for api calls to be made to.

Instead, we recommend you change the port for ``grouch`` to the standard port 80, map the ``webserver`` to a subdomain, and use a reverse-proxy to resolve the subdomain to an internal port. For example, lets say you have a static ip of 137.122.64.157 and a web domain of spfy.ca . You have an A Record that maps spfy.ca to 137.122.64.157. You could then expose port 80 externally on your host and map ``grouch`` to port 80 by setting:

.. code-block:: yaml

	ports:
	- "80:3000"

Port 8000 for ``webserver`` will still be available on your hosts loopback, but will not be exposed externally.
Add an A Record for api.spfy.ca to the same IP address, and then you could use an reverse-proxy such as Nginx to resolve api.spfy.ca to localhost:8000.

Setting a Subdomain
-------------------

This has to be done through the interface of your domain registrar. You'll have to add an Address Record (A Record), which is typically under the heading "Manage Advanced DNS Records" or similar.

Setting up a Reverse Proxy
--------------------------

We recommend you use NGINX as the reverse proxy. You can find their Getting Started guide at https://www.nginx.com/resources/wiki/start/

In addition, we recommend you use Certbot (part of the EFF's Let's Encrypt) project to get the required certificates and setup HTTPS on your server. You can find their interactive guide at https://certbot.eff.org/ which allow's you to specify the webserver (NGINX) and operating system you are using. Certbot comes with a nice script to automatically modify your NGINX configuration as required.

Point Reactapp to Your Subdomain
--------------------------------

To tell reactapp to point to your subdomain, you'll have to modify the ``api.js`` settings located at ``reactapp/src/middleware/api.js``.

The current ``ROOT`` of the target domain is:

.. code-block:: js

	const ROOT = window.location.protocol + '//' + window.location.hostname + ':8000/'
	
change this to:

.. code-block:: js

	const ROOT = 'https' + '//' + 'api.mydomain.com' + '/'
	
and then rebuild and redeploy reactapp.

.. code-block:: sh

	docker-compose build --no-cache reactapp
	docker-compose up -d

.. note::
e
	The Flask webserver has Cross-Origin Requests (CORS) enabled, so you can deploy reactapp to another server (that is only running reactapp, and not the webserver, databases, workers). The domain can be ``mydomain.com`` or any domain name you own - you'll just have to setup the A records as appropriate.

Deploying to Corefacility
=========================

Quick-Start
-----------

Use the ``production.sh`` script.
This script does a few things:

1. Stops the host Nginx so Docker can bind the ports it'll need for mapping.
2. Starts the Docker-Composition.
3. Restarts the host Nginx.
4. Starts Jetty which runs Blazegraph.

Important Volumes
-----------------

The ``webserver`` Docker container has a ``/datastore`` directory with all submitted files.

The ``mongodb`` Docker container has a ``/data/db`` directory which persists the ``Genome File Hash : SpfyID`` mapping.
(As well the ``?token=`` user sessions).

If you accidentally delete the MongoDB volume, it can be incrementally (when the same file is submitted, it will be re-cached) recreated from Blazegraph by setting ``DATABASE_EXISTING = True`` and ``DATABASE_BYPASS = False`` in ``app/config.py``.

Merging New Changes Into Production
-----------------------------------

The production-specific changes are committed to the local git history in corefacility.

Running:

.. code-block:: sh

	git merge origin/somebranch

will be sufficient to merge.

We can then rebuild and restart the composition:

.. code-block:: sh

	docker-compose build --no-cache
	./production.sh

Blazegraph
----------

Looking at the filesystem:

.. code-block:: sh

	[claing@superphy backend-4.3.3]$ df -h
	Filesystem                 Size  Used Avail Use% Mounted on
	/dev/mapper/superphy-root   45G   31G   14G  69% /
	devtmpfs                    12G     0   12G   0% /dev
	tmpfs                       12G  2.5G  9.3G  21% /dev/shm
	tmpfs                       12G   26M   12G   1% /run
	tmpfs                       12G     0   12G   0% /sys/fs/cgroup
	/dev/vda1                  497M  240M  258M  49% /boot
	/dev/mapper/docker-docker  200G   21G  180G  11% /docker
	warehouse:/ifs/Warehouse   769T  601T  151T  81% /Warehouse
	tmpfs                      2.4G     0  2.4G   0% /run/user/40151
	tmpfs                      2.4G     0  2.4G   0% /run/user/40290

``/Warehouse`` is used for long-term data storage and shared across the NML. In order to write to ``/Warehouse``, you need the permissions of either ``claing`` or ``superphy``; there are some problems with passing these permissions into Docker environments, so we run Blazegraph, inside of folder ``/Warehouse/Users/claing/superphy/spfy/docker-blazegraph/2.1.4-inferencing`` and as ``claing``, outside of Docker using:

.. code-block:: sh

	java -server -Xmx4g -Dbigdata.propertyFile=/Warehouse/Users/claing/superphy/spfy/docker-blazegraph/2.1.4-inferencing/RWStore.properties -jar blazegraph.jar

This command is run using ``screen`` allowing us to detach it from our shell.

.. code-block:: sh

	screen
	CTRL+a, d

and to resume:

.. code-block:: sh

	screen -r

See https://github.com/superphy/backend/issues/159

Docker Service
--------------

.. code-block:: sh

	[claing@superphy docker]$ sudo cat /etc/fstab

	#
	# /etc/fstab
	# Created by anaconda on Thu Dec 24 17:40:08 2015
	#
	# Accessible filesystems, by reference, are maintained under '/dev/disk'
	# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
	#
	/dev/mapper/superphy-root /                       xfs     defaults        1 1
	UUID=6c62e5cf-fd55-41e8-8122-e5e78643e3cd /boot                   xfs     defaults        1 2
	/dev/mapper/superphy-swap swap                    swap    defaults        0 0
	warehouse:/ifs/Warehouse	/Warehouse	nfs	defaults	0 0
	/dev/mapper/docker-docker /docker xfs defaults 1 2

Our root filesystem for the Corefacility VM is really small (45G) and we instead have a virtual drive at ``/dev/mapper/docker-docker`` which is mounted on ``/docker`` which has our Docker images / unmapped volumes. This is setup using symlinks:

.. code-block:: sh

	sudo systemctl stop docker
	cd /var/lib/
	sudo cp -rf docker/ /docker/backups/
	sudo rm -rf docker/
	sudo mkdir /docker/docker
	sudo ln -s /docker/docker /var/lib/docker
	sudo systemctl start docker

Docker Hub
----------

Docker Hub is used to host pre-built images; for us, this mostly consisting of our base ``docker-flask-conda`` image. The org. page is publically available at https://hub.docker.com/u/superphy/ and you can pull without any permission issues. To push a new image, first register an account at https://hub.docker.com/

The owner for the org. has the username ``superphyinfo`` and uses the same password as ``superphy.info@gmail.com``. You can use it to add yourself to the org.

You can then build and tag docker images to be pushed onto Docker Hub.

.. code-block:: sh

	docker build -f Dockerfile-reactapp -t superphy/reactapp:4.3.3-corefacility .

or tag an existing image:

.. code-block:: sh

	docker images
	docker tag 245d7e4bb63e superphy/reactapp:4.3.3-corefacility

Either way, you can then push using the same command:

.. code-block:: sh

	docker push superphy/reactapp:4.3.3-corefacility

.. note:: We occasionally use Docker Hub as a work-around in case a computer can't build an image. There is some bug where Corefacility VMs aren't connecting to NPM and thus we build the reactapp image on Cybera and pull it down on Corefacility.

Nginx
-----

We run Nginx above the Docker layer for 3 reasons:

	1. Handle the ``/superphy`` prefix to all our routes as we don't sure on ``/``
	2. To host both the original SuperPhy and Spfy on a single VM
	3. Buffer large file uploads before sending it to Spfy's Flask API

In ``/etc/nginx/nginx.conf``:

.. code-block:: nginx

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
	    error_log /var/log/nginx/error.log warn;

	    sendfile            on;
	    tcp_nopush          on;
	    tcp_nodelay         on;
	    keepalive_timeout   2m;
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
		client_max_body_size 60g;
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
	      	    proxy_pass http://localhost:8090;
	      	    proxy_redirect http://localhost:8090/ $scheme://$host/spfy/;
	     	    proxy_http_version 1.1;
	            proxy_set_header Upgrade $http_upgrade;
	      	    proxy_set_header Connection $connection_upgrade;
	      	    proxy_read_timeout 20d;
		}
		location /grouch/ {
	            rewrite ^/grouch/(.*)$ /$1 break;
	            proxy_pass http://localhost:8091;
	            proxy_redirect http://localhost:8091/ $scheme://$host/grouch/;
	            proxy_http_version 1.1;
	            proxy_set_header Upgrade $http_upgrade;
	            proxy_set_header Connection $connection_upgrade;
	            proxy_read_timeout 20d;
	        }
		location /shiny/ {
		    rewrite ^/shiny/(.*)$ /$1 break;
		    proxy_pass http://127.0.0.1:3838;
		    proxy_redirect http://127.0.0.1:3838/ $scheme://$host/shiny/;
		    proxy_http_version 1.1;
		    proxy_set_header Upgrade $http_upgrade;
		    proxy_set_header Connection $connection_upgrade;
		    proxy_read_timeout 950s;
		}

	    }

	    server {
	        client_max_body_size 60g;
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
		location = /grouch {
	            return 301 /superphy/grouch/;
	        }
	        location = /minio {
	            return 301 /superphy/minio/;
	        }
		location /spfy/ {
	            rewrite ^/spfy/(.*)$ /$1 break;
	            proxy_pass http://localhost:8090;
	            proxy_redirect http://localhost:8090/superphy/ $scheme://$host/spfy/;
	            proxy_http_version 1.1;
	            proxy_set_header Upgrade $http_upgrade;
	            proxy_set_header Connection $connection_upgrade;
	            proxy_read_timeout 20d;
	        }
		location /grouch/ {
	            rewrite ^/grouch/(.*)$ /$1 break;
	            proxy_pass http://localhost:8091;
	            proxy_redirect http://localhost:8091/superphy/ $scheme://$host/grouch/;
	            proxy_http_version 1.1;
	            proxy_set_header Upgrade $http_upgrade;
	            proxy_set_header Connection $connection_upgrade;
	            proxy_read_timeout 2h;
		    proxy_send_timeout 2h;
	        }
		location /shiny/ {
		    rewrite ^/shiny/(.*)$ /$1 break;
	            proxy_pass http://127.0.0.1:3838;
	            proxy_redirect http://127.0.0.1:3838/ $scheme://$host/shiny/;
	            proxy_http_version 1.1;
	            proxy_set_header Upgrade $http_upgrade;
	            proxy_set_header Connection $connection_upgrade;
		    proxy_read_timeout 950s;
		}
	    }


	}

Currently, this is setup to run the new Reactapp version of Spfy at https://lfz.corefacility.ca/superphy/grouch/ and the old AngularJS version + all the API endpoint at https://lfz.corefacility.ca/superphy/spfy/
This will probably change in the future, when backwards-incompatible changes are introduced to Spfy; we will run exclusively out of https://lfz.corefacility.ca/superphy/spfy/
The old SuperPhy is at https://lfz.corefacility.ca/superphy/

.. note:: There is an http://superphy.corefacility.ca/spfy/ address (but not a http://superphy.corefacility.ca/grouch/ address) that is only accessible from within the NML network (you'd have to VPN in if you're at the CFIA building), but we prefer to focus on the ``lfz.corefacility/superphy/`` routes which are available on both external/internal networks.

Some other points to note:

* The rewrite rules are critical to operating on Corefacility, as the ``/superphy/`` requirement can be tricky
* We're unsure if the ``client_max_body_size 60g;`` has any effect when deployed on Corefacility, it might be that there is another Nginx instance ran by the NML to route its VMs. Currently we're capped at ~250 MB uploads at a time on Corefacility, you can see a long debugging log of this at https://github.com/superphy/backend/issues/159
* Nginx is not hosting the websites, it only serves to proxy the requests to Apache (for the old SuperPhy) or Docker (for the new Spfy)

.. warning:: Nginx is also run internally in the Docker webserver image to allow you to handle running the composition by itself, but generally you shouldn't have to worry about it.
