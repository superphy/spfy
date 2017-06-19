===============
Developer Guide
===============

.. contents:: Table of Contents
   :local:

Getting Started
===============

We use Docker and Docker-Compose for managing the databases: Blazegraph and Redis, the webserver: Nginx/Flask/Conda, and Redis-Queue (RQ) workers: mostly in Conda. The official `Install Docker Compose guide`_ lists steps for installing both the base Docker Engine, and for installing Docker-Compose separately if you're on Linux. For Mac and Windows users, Docker-Compose comes bundled with Docker Engine.

You'll probably also want to `install Miniconda`_ as we bundle most dependencies in Conda environments.

.. _`Install Docker Compose guide`: https://docs.docker.com/compose/install/
.. _`install Miniconda`: https://conda.io/docs/install/quick.html

Terminology
-----------

====================  =====
Used Interchangeably  Notes
====================  =====
jobs, tasks           A job in RQ is typically called a task when discussing the front-end.
endpoint, api         We prefer to use endpoint for a route in Flask which the front-end interacts with.
====================  =====

Genome Files for testing
------------------------

For testing purposes, we use E.coli genome files from GenBank. A list of ftp
links is available at the `old github/semantic repo`_. There should be 5353
genome files in total a .zip of which is available within the NML.

.. _`old github/semantic repo`: https://raw.githubusercontent.com/superphy/semantic/master/superphy/src/upload/python/data/download_files.txt

Docker Caveats
--------------

We've had problems with Ubuntu Desktop versions 16.04.2 LTS and 17.04 not connecting to NPM when building Docker images and from within the building. Builds work fine with Ubuntu Server 16.04.2 LTS on Cybera and for Ubuntu Server 12.04 or 14.04 LTS on Travis-CI. Within the building, RHEL-based operating systems (CentOS / Scientific Linux) build our NPM-dependent images (namely, `reactapp`_) just fine.

For RHEL-based OSs, I don't recommend using `devicemapper`, but instead use `overlayfs`. Reasons are documented at https://github.com/moby/moby/issues/3182. There is a guide on setting up Docker with `overlayfs` at https://dcos.io/docs/1.7/administration/installing/custom/system-requirements/install-docker-centos/, though I haven't personally tested it.

If you do end up using `devicemapper` and run into disk space issues, such as:

.. code-block:: bash

  172.18.0.1 - - [05/Jun/2017:17:50:01 +0000] "GET / HTTP/1.1" 200 12685 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" "-"
  2017/06/05 17:50:13 [warn] 11#11: *2 a client request body is buffered to a temporary file /var/cache/nginx/client_temp/0000000001, client: 172.18.0.1, server: , request: "POST /upload HTTP/1.1", host: "localhost:8000", referrer: "http://localhost:8000/"
  [2017-06-05 17:58:31,417] ERROR in app: Exception on /upload [POST]
  Traceback (most recent call last):
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1982, in wsgi_app
      response = self.full_dispatch_request()
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1614, in full_dispatch_request
      rv = self.handle_user_exception(e)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask_cors/extension.py", line 161, in wrapped_function
      return cors_after_request(app.make_response(f(*args, **kwargs)))
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1517, in handle_user_exception
      reraise(exc_type, exc_value, tb)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1612, in full_dispatch_request
      rv = self.dispatch_request()
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/app.py", line 1598, in dispatch_request
      return self.view_functions[rule.endpoint](**req.view_args)
    File "./routes/views.py", line 86, in upload
      form = request.form
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/local.py", line 343, in __getattr__
      return getattr(self._get_current_object(), name)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/utils.py", line 73, in __get__
      value = self.func(obj)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/wrappers.py", line 492, in form
      self._load_form_data()
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/flask/wrappers.py", line 185, in _load_form_data
      RequestBase._load_form_data(self)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/wrappers.py", line 361, in _load_form_data
      mimetype, content_length, options)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 195, in parse
      content_length, options)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 100, in wrapper
      return f(self, stream, *args, **kwargs)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 212, in _parse_multipart
      form, files = parser.parse(stream, boundary, content_length)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 523, in parse
      return self.cls(form), self.cls(files)
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/datastructures.py", line 384, in __init__
      for key, value in mapping or ():
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 521, in <genexpr>
      form = (p[1] for p in formstream if p[0] == 'form')
    File "/opt/conda/envs/backend/lib/python2.7/site-packages/werkzeug/formparser.py", line 497, in parse_parts
      _write(ell)
  IOError: [Errno 28] No space left on device
  [pid: 44|app: 0|req: 2/2] 172.18.0.1 () {46 vars in 867 bytes} [Mon Jun  5 17:53:08 2017] POST /upload => generated 291 bytes in 323526 msecs (HTTP/1.1 500) 2 headers in 84 bytes (54065 switches on core 0)
  172.18.0.1 - - [05/Jun/2017:17:58:32 +0000] "POST /upload HTTP/1.1" 500 291 "http://localhost:8000/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" "-"

Which was displayed by running:

.. code-block:: bash

  docker-compose logs backend_webserver_1

You will have to increase the volume disk sizes: https://forums.docker.com/t/increase-container-volume-disk-size/1652/8

.. code-block:: bash

  # With Centos 7 I did the following to increase the default size of the containers
  # Modify the docker config in /etc/sysconfig/docker-storage to add the line:
  DOCKER_STORAGE_OPTIONS= - -storage-opt dm.basesize=20G
  service docker stop
  rm /var/lib/docker NOTE THIS DELETES ALL IMAGES etc. SO MAKE A BACKUP
  service docker start
  docker load < [each_save_in_backup.tar]
  docker run -i -t [imagename] /bin/bash
  # In the bash prompt of the docker container "df -k" should show 20GB / file system size now.

Adding a New Module
===================

There are two ways of adding a new module:

1. Integrate your code into the Spfy codebase and update the RQ workers accordingly.
2. Create a new Docker image with your code, and setup a new Queue name for your module.

If you wish to integrate your code with Spfy, you'll have to update any dependencies to the underlying Conda-based image the RQ workers depend on. You'll also have to include your code in the `/app` directory of this repo, as that is the only directory the current RQ workers contain. The intended structure is to create a directory in `/app/modules` for your codebase and a `.py` file above at `/app/modules/newmodule.py`, for example, which contains the method your `Queue.enqueue()` function uses.

There is more specific documentation for this process in `Directly Adding a New Module`_.

If you wish to create your own image, you can use the RQ `worker`_ image as a starting point. Specifically you'll want to add your repo as a git submodule in `superphy/backend` and modify the `COPY ./app /app` to target your repo, similar to the way `reactapp`_ is included. You'll also want to take a look at the `supervisord-rq.conf`_ which controls the RQ workers. Specifically, the `command=/opt/conda/envs/backend/bin/rq worker -c config multiples` would have to be modified to target the name of the new Queue your container listens to; by replacing `multiples` with `newqueue`, for example.

There is more specific documentation for this process in `Indirectly Adding a New Module`_.

In both cases, the spfy webserver will have to be modified in order for the front-end to have an endpoint target; this is documented in `Adding an Endpoint in Flask`_. The front-end will also have to be modified for there to be a form to submit tasks and have a results view generated for your new module; this is documented in `Modifying the Front-End`_.

Adding an Endpoint in Flask
---------------------------

Modifying the Front-End
-----------------------

.. _`reactapp`: https://github.com/superphy/reactapp
.. _`supervisord-rq.conf`: https://github.com/superphy/backend/blob/master/app/supervisord-rq.conf

Directly Adding a New Module
============================

Adding Dependencies via Conda
-----------------------------

The main `environment.yml`_ file is located in our `superphy/docker-flask-conda`_
repo. This is used by the `worker`_ and `worker-blazegraph-ids`_ containers
(and the `webserver`_ container, though that may/should change). We also pull
this base superphy/docker-flask-conda image from Docker Hub. So you would have
to:

1. push the new image
2. specify the new version on each Dockerfile, namely via the

.. code-block:: bash

  FROM superphy/docker-flask-conda:2.0.0

tag.

.. _`environment.yml`: https://raw.githubusercontent.com/superphy/docker-flask-conda/master/app/environment.yml
.. _`superphy/docker-flask-conda`: https://github.com/superphy/docker-flask-conda
.. _`worker`: https://github.com/superphy/backend/blob/master/Dockerfile-rq
.. _`worker-blazegraph-ids`: https://github.com/superphy/backend/blob/master/Dockerfile-rq-blazegraph
.. _`webserver`: https://github.com/superphy/backend/blob/master/Dockerfile-spfy

Integrating your Codebase into Spfy
-----------------------------------

Indirectly Adding a New Module
==============================

Adding your Repo as a Git Submodule
-----------------------------------

Picking a Base Docker Image
---------------------------

Adding your Dependencies
------------------------

Updating Docker-Compose.yml
---------------------------
