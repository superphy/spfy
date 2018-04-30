===============
Developer Guide
===============

.. contents:: Table of Contents
   :local:

Getting Started
===============

Don't worry, genome files are just like Excel spreadsheets.

.. image:: algorithms.png
    :align: center
    :alt: excel is complicated

(from the excellent https://xkcd.com/)

We use Docker and Docker-Compose for managing the databases: Blazegraph and Redis, the webserver: Nginx/Flask/Conda, and Redis-Queue (RQ) workers: mostly in Conda. The official `Install Docker Compose guide`_ lists steps for installing both the base Docker Engine, and for installing Docker-Compose separately if you're on Linux. For Mac and Windows users, Docker-Compose comes bundled with Docker Engine.

You'll probably also want to `install Miniconda`_ as we bundle most dependencies in Conda environments. Specific instructions to Spfy are available at `Installing Miniconda`_.

Note that there is a `Debugging`_ section for tracking down the source of problems you may encounter.

.. _`Install Docker Compose guide`: https://docs.docker.com/compose/install/
.. _`install Miniconda`: https://conda.io/docs/install/quick.html

Terminology
-----------

====================  =====
Used Interchangeably  Notes
====================  =====
jobs, tasks           A job in RQ is typically called a task when discussing the front-end.
endpoint, api         We prefer to use endpoint for a route in Flask which the front-end interacts with.
spfy, this repo       The superphy/backend repo.
====================  =====

Reading
-------

For the libraries you're not familiar with, we recommend you skim the docs below before starting:

* An overview of HTTP requests: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
* Flask Blueprints (for routes): http://exploreflask.com/en/latest/blueprints.html
* Redis Queue docs: http://python-rq.org/docs/
* Thinking In React: https://facebook.github.io/react/docs/thinking-in-react.html
* JSX In Depth: https://facebook.github.io/react/docs/jsx-in-depth.html

Reference Docs
--------------

Javascript:

* Yarn commands for npm users: https://yarnpkg.com/lang/en/docs/migrating-from-npm/
* React Material Design docs: https://react-md.mlaursen.com/components/text-fields
* React-Bootstrap-Table docs: https://allenfang.github.io/react-bootstrap-table/example.html#basic

Installing Miniconda
--------------------

For Linux-64 based distros, grab the Pyhon 2.7 Miniconda install script and install it (be sure to select the option to add Miniconda's path for your .bashrc):

.. code-block:: sh

  wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
  bash Miniconda2-latest-Linux-x86_64.sh

Then get, install, and activate our Conda environment.yml:

.. code-block:: sh

  wget https://raw.githubusercontent.com/superphy/docker-flask-conda/master/app/environment.yml
  conda env create -f environment.yml
  source activate backend

Genome Files for testing
------------------------

For testing purposes, we use E.coli genome files from GenBank. A list of ftp
links is available at the `old github/semantic repo`_. There should be 5353
genome files in total a .zip of which is available within the NML.

.. _`old github/semantic repo`: https://raw.githubusercontent.com/superphy/semantic/master/superphy/src/upload/python/data/download_files.txt

Generating More Genomes for Testing
-----------------------------------

The main points to keep in mind is that Spfy runs quality control checks to ensure submissions are E.coli and that hash checking is employed to avoid duplicate entries in the datbase.
The way we generate fakes are using a seed folder of actual genomes (to pass QC) and renmaing the contig headers (to pass hash checking).

Usage:

1. Activate the conda env described in `Installing Miniconda`_.
2. cd in ``backend/scripts/`` (not: ```backend/app/scripts``)
3. Run: ``python generate_fakegenomes.py -i ~/ecoli-genomes/ -n 50000`` where ``-i`` gives the seed folder and ``-n`` gives the number of genomes to generate. This will put all the fakes in ``~/ecoli-genomes/fakes/``.

Docker Caveats
--------------

We've had problems in the past with Ubuntu Desktop versions 16.04.2 LTS and 17.04, and Ubuntu Server 16.04.2 LTS not connecting to NPM when building Docker images and from within the building. Builds work fine with Ubuntu Server 16.04.2 LTS on Cybera and for Ubuntu Server 12.04 and 14.04 LTS on Travis-CI. Within the building, RHEL-based operating systems (CentOS / Scientific Linux) build our NPM-dependent images (namely, `reactapp`_) just fine. Tested the build at home on Ubuntu Server 16.04.2 LTS and it works fine - looks like this is isolated to within the buildng @NML Lethbridge.

.. warning:: As of June 30, 2017 Ubuntu Server 16.04.2 LTS is building NPM-dependent images okay @NML Lethbridge.

.. note:: In general, we recommend you run Docker on Ubuntu 16.04.2 LTS (Server or Desktop) if you're outside the NML's Lethrbidge location. Otherwise, CentOS is a secondary option.

For RHEL-based OSs, I don't recommend using `devicemapper`, but instead use `overlayfs`. Reasons are documented at https://github.com/moby/moby/issues/3182. There is a guide on setting up Docker with `overlayfs` at https://dcos.io/docs/1.7/administration/installing/custom/system-requirements/install-docker-centos/, though I haven't personally tested it.
UPDATE: (June 22'17) There is a guide written by a Red Hat dev. http://www.projectatomic.io/blog/2015/06/notes-on-fedora-centos-and-docker-storage-drivers/

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

Redis
-----

.. warning:: By default, our docker composition is setup to run Redis db with persistant storage so jobs are kept even in you stop and restart the ``redis`` service. This is useful in production and regular usage scenarios as all your jobs are not lost if the composition is stopped or the server/computer is rebooted. However, this also means that if you write a job which errors out and also upload a bunch of files, they will continue to be started even if you stop the composition to write fixes.

To run Redis in non-persistant mode, in ``docker-compose.yml`` replace:

.. code-block:: yaml

  redis:
    image: redis:3.2
    command: redis-server --appendonly yes # for persistance
    volumes:
    - /data

with:

.. code-block:: yaml

  redis:
    image: redis:3.2

The General Workflow
--------------------

.. note:: To use ``docker-compose`` commands, you must be in the same directory as the ``docker-compose.yml`` file you're trying to work with. This is because Docker-Compose uses that .yml file to determine the names of services you're running commands against; for example you might run ``docker-compose logs webserver``. You can still access the underlying docker containers outside of the folder by interfacing with the docker engine directly: ``docker logs backend_webserver_1``.

For working on the backend:

1. Make your changes/additions
2. Rebuild the images

  .. code-block:: sh

    docker-compose build --no-cache

  or selectively:

  .. code-block:: sh

    docker-compose build --no-cache webserver worker

3. Bring up the composition and use Chrome's devtools for testing

  .. code-block:: sh

    docker-compose up

4. Check logs as appropriate:

  .. code-block:: sh

    docker-compose logs webserver
    docker-compose logs worker

5. Cleanup the composition you just started

  .. code-block:: sh

    docker-compose down

6. Make more changes and rebuild

  .. code-block:: sh

    docker-compose build --no-cache

For working on the front-end:

We reccomend using ``yarn start`` as it has hot-reloading enabled so it'll automatically rebuild and display your changes at ``localhost:3000``.

1. First, start up the backend (if you're now making changes to the backend, we'll use the default build step when bringing up the composition)

  .. code-block:: sh

    docker-compose up

2. In a separate terminal, fork and clone the reactapp repo, and then bring it up (you'll have to install ``node`` and ``yarn``:

  .. code-block:: sh

    yarn install
    yarn start

3. Make changes to your fork of reactapp and you'll see them refreshed live at ``localhost:3000``.

Adding a New Module
===================

There are a few ways of adding a new module:

1. Integrate your code into the Spfy codebase and update the RQ workers accordingly.
2. Add a enqueuing method to Spfy's code, but then create a new queue and a new docker image, with additional dependencies, which is added to Spfy's docker-compose.yml file.
3. Setting up your module as a microservice running in its own Docker container, add a worker to handle requests to RQ.

.. note:: The quickest approach is to integrate your code into the Spfy codebase and update the RQ workers accordingly.

If you wish to integrate your code with Spfy, you'll have to update any dependencies to the underlying Conda-based image the RQ workers depend on. You'll also have to include your code in the `/app` directory of this repo, as that is the only directory the current RQ workers contain. The intended structure is to create a directory in `/app/modules` for your codebase and a `.py` file above at `/app/modules/newmodule.py`, for example, which contains the method your `Queue.enqueue()` function uses.

There is more specific documentation for this process in `Directly Adding a New Module`_.

If you wish to create your own image, you can use the RQ `worker`_ image as a starting point. Specifically you'll want to add your repo as a git submodule in `superphy/backend` and modify the `COPY ./app /app` to target your repo, similar to the way `reactapp`_ is included. You'll also want to take a look at the `supervisord-rq.conf`_ which controls the RQ workers.

In both cases, the spfy webserver will have to be modified in order for the front-end to have an endpoint target; this is documented in `Adding an Endpoint in Flask`_. The front-end will also have to be modified for there to be a form to submit tasks and have a results view generated for your new module; this is documented in `Modifying the Front-End`_.

Directly Adding a New Module
============================

.. warning:: Everything (rq workers, uwsgi, etc.) run inside ``/app``, and all python imports should be relative to this. Such as

.. code-block:: python

  from middleware.blazegraph.reserve_id import reserve_id

The top-most directory is used to build Docker Images and copies the contents of ``/app`` to run inside the containers. This is done as the apps (Flask, Reactapp) themselves don't need copies of the Dockerfiles, other apps, etc.

About the Existing Codebase
---------------------------

If you want to store the results to Blazegraph, you can add that to your pipeline. For subtyping tasks (ECTyper, RGI), the graph generation is handled in ``/app/modules/turtleGrapher/datastruct_savvy.py``, you can use that as an example. Note that the ``upload_graph()`` call is made within ``datastruct_savvy.py``; this is done to avoid having to pass the resulting ``rdflib.Graph`` object between tasks.
Also, the base graph (only containing information about the file, without any results from analyses) is handled by ``/app/modules/turtleGrapher/turtle_grapher.py``.

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

To get started, `install Miniconda`_ and clone the docker-flask-conda repo:

.. code-block:: sh

  git clone https://github.com/superphy/docker-flask-conda.git && cd docker-flask-conda

Recreate the env:

.. code-block:: sh

  conda env create -f app/environment.yml

Activate the env:

.. code-block:: sh

  source activate backend

Then you can install any dependencies as usual.
Via pip:

.. code-block:: sh

  pip install whateverpackage

or conda

.. code-block:: sh

  conda install whateverpackage

You can then export the env:

.. code-block:: sh

  conda env export > app/environment.yml

If you push your changes to github on `master`, Travis-CI is setup to build the Docker Image and push it to Docker Hub automatically under the tag `latest`.

Otherwise, build and push the image under your own tag, for example `0.0.1`:

.. code-block:: sh

  docker build -t superphy/docker-flask-conda:0.0.1 .
  docker push superphy/docker-flask-conda:0.0.1

Then specific your image in the corresponding Dockerfiles: `worker`_. If you're adding dependencies to flask, also update the `webserver`_ Dockerfile.

.. code-block:: bash

  FROM superphy/docker-flask-conda:0.0.1

.. _`environment.yml`: https://raw.githubusercontent.com/superphy/docker-flask-conda/master/app/environment.yml
.. _`superphy/docker-flask-conda`: https://github.com/superphy/docker-flask-conda
.. _`worker`: https://github.com/superphy/backend/blob/master/Dockerfile-rq
.. _`worker-blazegraph-ids`: https://github.com/superphy/backend/blob/master/Dockerfile-rq-blazegraph
.. _`webserver`: https://github.com/superphy/backend/blob/master/Dockerfile-spfy

Integrating your Codebase into Spfy
-----------------------------------

There are two ways of approaching this:

1. If you're not using any of Spfy's codebase, add your code as a git submodule in `/app/modules/`
2. If you are using Spfy's codebase, fork and create a directory in `/app/modules/` with your code.

In both cases, you should add a method in `/app/module/pickaname.py` which enqueues a call to your package. More information on this is documented at `Enqueing a Job to RQ`_.

To add a git submodule, clone the repo and create a branch:

.. code-block:: sh

  git clone --recursive https://github.com/superphy/backend.git && cd backend/
  git checkout -b somenewmodule

You can then add your repo and commit it to `superphy/backend` as usual:

.. code-block:: sh

  git submodule add https://github.com/chaconinc/DbConnector app/modules/DbConnector
  git add .
  git commit -m 'ADD: my new module'

or a specific branch:

.. code-block:: sh

  git submodule add -b somebranch https://github.com/chaconinc/DbConnector app/modules/DbConnector

Note that the main repo `superphy/backend` will pin your git submodule to a specific commit. You can update it to the HEAD of w/e branch was used by running a `git pull` from within the submodule's directory and then adding it in the main repo. If you push this change to GitHub, to update other clones of superphy/backend run:

.. code-block:: sh

  git submodule update

Adding an Endpoint in Flask
===========================

To create a new endpoint in Flask, you'll have to:

1. Create a Blueprint with your route(s) and register it to the app.
2. Enqueue a job in RQ
3. Return the job id via Flask to the front-end

We recommend you perform the setup in `Monitoring RQ`_ before you begin.

Creating a Blueprint
--------------------

We use `Flask Blueprints`_ to compartmentalize all routes. They are contained in `/app/routes` and have the following basic structure:

.. code-block:: python

  from flask import Blueprint, request, jsonify

  bp_someroutes = Blueprint('someroutes', __name__)

  # if methods is not defined, default only allows GET
  @bp_someroutes.route('/api/v0/someroute', methods=['POST'])
  def someroute():
    form = request.form
    return jsonify('Got your form')

Note that a blueprint can have multiple routes defined in it such as in `ra_views.py`_ which is used to build the group options for Fisher's comparison. To add a new route, create a python file such as `/app/routes/someroutes.py` with the above structure. Then in the app `factory.py`_ import your blueprint via:

.. code-block:: python

  from routes.someroute import bp_someroute

and register your blueprint in `create_app()` by adding:

.. code-block:: python

  app.register_blueprint(bp_someroute)

Note that we allow CORS on all routes of form `/api/*` such as `/api/v0/someroute`. This is required as the front-end `reactapp`_ is deployed in a separate container (and has a separate IP Address) from the Flask app.

.. _`Flask Blueprints`: http://flask.pocoo.org/docs/0.12/blueprints/
.. _`ra_views.py`: https://github.com/superphy/backend/blob/master/app/routes/ra_views.py
.. _`factory.py`: https://github.com/superphy/backend/blob/master/app/factory.py

Enqueing a Job to RQ
--------------------

You will then have to enqueue a job, based off that request form. There is an example of how form parsing is handled for Subtyping in the `upload()` method of `ra_posts.py`_.

If you're integrating your codebase with Spfy, add your code to a new directory in `/app/modules` and a method which handles enqueing in `/app/modules/somemodule.py` for example. The `gc.py`_ file resembles a basic template for a method to enqueue.

.. code-block:: python

  import logging
  import config
  import redis
  from rq import Queue
  from modules.comparisons.groupcomparisons import groupcomparisons
  from modules.loggingFunctions import initialize_logging

  # logging
  log_file = initialize_logging()
  log = logging.getLogger(__name__)

  redis_url = config.REDIS_URL
  redis_conn = redis.from_url(redis_url)
  multiples_q = Queue('multiples', connection=redis_conn, default_timeout=600)

  def blob_gc_enqueue(query, target):
      job_gc = multiples_q.enqueue(groupcomparisons, query, target, result_ttl=-1)
      log.info('JOB ID IS: ' + job_gc.get_id())
      return job_gc.get_id()

Of note is that when calling RQ's enqueue() method, a custom Job class is returned. It is important that our enqueuing method returns the job id to flask, which is typically some hash such as:

.. code-block:: python

  16515ba5-040d-4315-9c88-a3bf5bfbe84e

Returning the Job ID to the Front-End
-------------------------------------

Generally, we expect the return from Flask (to the front-end) to be a dictionary with the job id as the key to another dictionary with keys `analysis` and `file` (if relevant), though this is not strictly required (a single line containing the key will also work, as you handle naming of analysis again when doing a `dispatch()` in `reactapp`_ - more on this later). For example, a return might be:

.. code-block:: python

  "c96619b8-b089-4a3a-8dd2-b09b5d5e38e9": {
    "analysis": "Virulence Factors and Serotype",
    "file": "/datastore/2017-06-14-21-26-43-375215-GCA_001683595.1_NGF2_genomic.fna"
  }

It is expected that only 1 job id be returned per request. In `v4.2.2`_ we introduced the concept of `blob` ids in which dependency checking is handled server-side; you can find more details about this in `reactapp issue #30`_ and `backend issue #90`_. The Redis DB was also set to run in persistent-mode, with results stored to disk inside a docker volume. The `blob` concept is only relevant if you handle parallelism & pipelines for a given task (ex. Subtyping) through multiple RQ jobs (ex. QC, ID Reservation, ECTyper, RGI, parsing, etc.); if you handle parallelism in your own codebase, then this isn't required.

Another point to note is that the:

.. code-block:: python

  result_ttl=-1

parameter in the `enqueue()` method is required to store the result in Redis permanently; this is done so results will forever be available to the front-end. If we ever scale Spfy to widespread usage, it may be worth setting a ttl of 48 hours or so via:

.. code-block:: python

  result_ttl=172800

where the ttl is measured in seconds. A warning message would also have to be added to `reactapp`_.

.. _`ra_posts.py`: https://github.com/superphy/backend/blob/master/app/routes/ra_posts.py
.. _`v4.2.2`: https://github.com/superphy/backend/releases/tag/v4.2.2
.. _`reactapp issue #30`: https://github.com/superphy/reactapp/issues/30
.. _`backend issue #90`: https://github.com/superphy/backend/issues/90
.. _`gc.py`: https://github.com/superphy/backend/blob/master/app/modules/gc.py

Seeing Your Changes in Docker
-----------------------------

To rebuild the Flask image, in `/backend`:

.. code-block:: sh

  docker-compose stop webserver worker
  docker-compose build --no-cache webserver worker
  docker-compose up

Optional: Adding a new Queue
============================

Normally, we distribute tasks between two main queues: `singles` and `multiples`. The singles queue is intended for tasks that can't be run in parallel within the same container (though you can probably run multiple containers, if you so wish); our use-case is for ECTyper. Everything else is intended to be run on the `multiples` queue.

If you wish to add your own Queue, you'll have to create some worker to listen to it. Ideally, do this by creating a new Docker container for your worker by copying the `worker`_ Dockerfile as your starting point then copying and modifying the `supervisord-rq.conf`_ to listen to your new queue. Specifically, the:

.. code-block:: bash

  command=/opt/conda/envs/backend/bin/rq worker -c config multiples

would have to be modified to target the name of the new Queue your container listens to; by replacing `multiples` with `newqueue`, for example.

Eventually, we may wish to add priority queues once the number of tasks become large and we have long-running tasks alongside ones that should immediately return to the user. This can be defined by the order in which queues are named in the supervisord command:

.. code-block:: bash

  command=/opt/conda/envs/backend/bin/rq worker -c config multiples

For example, queues `dog` and `cat` can be ordered:

.. code-block:: bash

  command=/opt/conda/envs/backend/bin/rq worker -c config dog cat

which instructs the RQ workers to run tasks in `dog` first, before running tasks in `cat`.

Modifying the Front-End
=======================

I'd recommend you leave Spfy's setup running in Docker-Compose and run the reactapp live so you can see immediate updates.

To get started, `install node`_ and then `install yarn`_. For debugging, I also recommend using Google Chrome and installing the `React Dev Tools`_ and `Redux Dev Tools`_.

.. _`React Dev Tools`: https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi?hl=en
.. _`Redux Dev Tools`: https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=en

  Optionally, I like to run Spfy's composition on one of the Desktops while coding away on my laptop. You can do the same by modifying `ROOT` api address in `api.js`_ to point to a different IP address or name:

  .. code-block:: jsx

    const ROOT = 'http://10.139.14.212:8000/'

Then, with Spfy's composition running, you'll want to clone `reactapp`_ and run:

.. code-block:: bash

  cd reactapp/
  yarn install
  yarn start

Our `reactapp`_ uses `Redux` to store jobs, but also uses regular `React states` when building forms or displaying results. This was done so you don't have to be too familiar with Redux when building new modules. The codebase is largely JSX+ES6.

Adding a New Task Card
----------------------

The first thing you'll want to do is add a description of your module to `api.js`_. For example, the old analyses const is:

.. code-block:: jsx

  export const analyses = [{
    'analysis':'subtyping',
    'description':'Serotype, Virulence Factors, Antimicrobial Resistance',
    'text':(
      <p>
        Upload genome files & determine associated subtypes.
        <br></br>
        Subtyping is powered by <a href="https://github.com/phac-nml/ecoli_serotyping">ECTyper</a>.
        AMR is powered by <a href="https://card.mcmaster.ca/analyze/rgi">CARD</a>.
      </p>
    )
  },{
    'analysis':'fishers',
    'description':"Group comparisons using Fisher's Exact Test",
    'text':'Select groups from uploaded genomes & compare for a chosen target datum.'
  }]

If we added a new module called `ml`, analyses might be:

.. code-block:: jsx

  export const analyses = [{
    'analysis':'subtyping',
    'description':'Serotype, Virulence Factors, Antimicrobial Resistance',
    'text':(
      <p>
        Upload genome files & determine associated subtypes.
        <br></br>
        Subtyping is powered by <a href="https://github.com/phac-nml/ecoli_serotyping">ECTyper</a>.
        AMR is powered by <a href="https://card.mcmaster.ca/analyze/rgi">CARD</a>.
      </p>
    )
  },{
    'analysis':'fishers',
    'description':"Group comparisons using Fisher's Exact Test",
    'text':'Select groups from uploaded genomes & compare for a chosen target datum.'
  },{
    'analysis':'ml',
    'description': "Machine learning module for Spfy",
    'text': 'Multiple machine learning algorithms such as, support vector machines, naive Bayes, and the Perceptron algorithm.'
  }]

This will create a new card for in tasks at the root page.

Adding a New Task Form
----------------------

.. note:: On terminology: we consider `containers` to be *Redux-aware*; that is, they require the `connect()` function from `react-redux`. `Components` are generally not directly connected to Redux and instead get information from the Redux store passed down to it via the component's `props`. Note that this is not strictly true as we make use of `react-refetch`, which is a fork of Redux and uses a separate `connect()` function, to poll for job statuses and results. However, the interaction between `react-refetch` and `redux` is largely abstracted away from you and instead maps a components props directly to updates via `react-refetch` - you don't have to dispatch actions or pull down updates separately.

Then create a container in `/src/containers` which will be your request form. You can look at `Subtyping.js`_ for an example.

.. code-block:: jsx

  import React, { PureComponent } from 'react';
  // react-md
  import FileInput from 'react-md/lib/FileInputs';
  import Checkbox from 'react-md/lib/SelectionControls/Checkbox'
  import TextField from 'react-md/lib/TextFields';
  import Button from 'react-md/lib/Buttons';
  import Switch from 'react-md/lib/SelectionControls/Switch';
  import Subheader from 'react-md/lib/Subheaders';
  import CircularProgress from 'react-md/lib/Progress/CircularProgress';
  // redux
  import { connect } from 'react-redux'
  import { addJob } from '../actions'
  import { subtypingDescription } from '../middleware/subtyping'
  // axios
  import axios from 'axios'
  import { API_ROOT } from '../middleware/api'
  // router
  import { Redirect } from 'react-router'
  import Loading from '../components/Loading'

  class Subtyping extends PureComponent {
    constructor(props) {
      super(props);
      this.state = {
        file: null,
        pi: 90,
        amr: false,
        serotype: true,
        vf: true,
        submitted: false,
        open: false,
        msg: '',
        jobId: "",
        hasResult: false,
        groupresults: true,
        progress: 0
      }
    }
    _selectFile = (file) => {
      console.log(file)
      if (!file) { return; }
      this.setState({ file });
    }
    _updatePi = (value) => {
      this.setState({ pi: value });
    }
    _updateSerotype = (value) => {
      this.setState({ serotype: value })
    }
    _updateAmr = (value) => {
      this.setState({ amr: value })
    }
    _updateVf = (value) => {
      this.setState({ vf: value })
    }
    _updateGroupResults = (groupresults) => {
      this.setState({ groupresults })
    }
    _updateUploadProgress = ( progress ) => {
      this.setState({progress})
    }
    _handleSubmit = (e) => {
      e.preventDefault() // disable default HTML form behavior
      // open and msg are for Snackbar
      // uploading is to notify users
      this.setState({
        uploading: true
      });
      // configure a progress for axios
      const createConfig = (_updateUploadProgress) => {
        var config = {
          onUploadProgress: function(progressEvent) {
            var percentCompleted = Math.round( (progressEvent.loaded * 100) / progressEvent.total );
            _updateUploadProgress(percentCompleted)
          }
        }
        return config
      }
      // create form data with files
      var data = new FormData()
      // eslint-disable-next-line
      this.state.file.map((f) => {
        data.append('file', f)
      })
      // append options
      // to match spfy(angular)'s format, we dont use a dict
      data.append('options.pi', this.state.pi)
      data.append('options.amr', this.state.amr)
      data.append('options.serotype', this.state.serotype)
      data.append('options.vf', this.state.vf)
      // new option added in 4.2.0, group all files into a single result
      // this means polling in handled server-side
      data.append('options.groupresults', this.state.groupresults)
      // put
      axios.post(API_ROOT + 'upload', data, createConfig(this._updateUploadProgress))
        .then(response => {
          console.log(response)
          // no longer uploading
          this.setState({
            uploading: false
          })
          let jobs = response.data
          // handle the return
          for(let job in jobs){
            let f = (this.state.file.length > 1 ?
            String(this.state.file.length + ' Files')
            :this.state.file[0].name)
            if(jobs[job].analysis === "Antimicrobial Resistance"){
              this.props.dispatch(addJob(job,
                "Antimicrobial Resistance",
                new Date().toLocaleTimeString(),
                subtypingDescription(f, this.state.pi, false, false, this.state.amr)
              ))
            } else if (jobs[job].analysis === "Virulence Factors and Serotype") {
              let descrip = ''
              if (this.state.vf && this.state.serotype){descrip = "Virulence Factors and Serotype"}
              else if (this.state.vf && !this.state.serotype) {descrip = "Virulence Factors"}
              else if (!this.state.vf && this.state.serotype) {descrip = "Serotype"}
              this.props.dispatch(addJob(job,
                descrip,
                new Date().toLocaleTimeString(),
                subtypingDescription(f, this.state.pi, this.state.serotype, this.state.vf, false)
              ))
            } else if (jobs[job].analysis === "Subtyping") {
              // set the jobId state so we can use Loading
              const jobId = job
              this.setState({jobId})
              // dispatch
              this.props.dispatch(addJob(job,
                "Subtyping",
                new Date().toLocaleTimeString(),
                subtypingDescription(
                  f , this.state.pi, this.state.serotype, this.state.vf, this.state.amr)
              ))
            }
          }
          const hasResult = true
          this.setState({hasResult})
        })
    };
    render(){
      const { file, pi, amr, serotype, vf, groupresults, uploading, hasResult, progress } = this.state
      return (
        <div>
          {/* uploading bar */}
          {(uploading && !hasResult) ?
            <div>
              <CircularProgress key="progress" id="loading" value={progress} centered={false} />
              Uploading... {progress} %
            </div>
            : ""
          }
          {/* actual form */}
          {(!hasResult && !uploading)?
            <form className="md-text-container md-grid">
              <div className="md-cell md-cell--12">
                <FileInput
                  id="inputFile"
                  secondary
                  label="Select File(s)"
                  onChange={this._selectFile}
                  multiple
                />
                <Switch
                  id="groupResults"
                  name="groupResults"
                  label="Group files into a single result"
                  checked={groupresults}
                  onChange={this._updateGroupResults}
                />
                {!groupresults ?
                  <Subheader primaryText="(Will split files & subtyping methods into separate results)" inset />
                : ''}
                <Checkbox
                  id="serotype"
                  name="check serotype"
                  checked={serotype}
                  onChange={this._updateSerotype}
                  label="Serotype"
                />
                <Checkbox
                  id="vf"
                  name="check vf"
                  checked={vf}
                  onChange={this._updateVf}
                  label="Virulence Factors"
                />
                <Checkbox
                  id="amr"
                  name="check amr"
                  checked={amr}
                  onChange={this._updateAmr}
                  label="Antimicrobial Resistance"
                />
                {amr ?
                  <Subheader primaryText="(Note: AMR increases run-time by several minutes per file)" inset />
                : ''}
                <TextField
                  id="pi"
                  value={pi}
                  onChange={this._updatePi}
                  helpText="Percent Identity for BLAST"
                />
                <Button
                  raised
                  secondary
                  type="submit"
                  label="Submit"
                  disabled={!file}
                  onClick={this._handleSubmit}
                />
              </div>
              <div className="md-cell md-cell--12">
                {this.state.file ? this.state.file.map(f => (
                  <TextField
                    key={f.name}
                    defaultValue={f.name}
                  />
                )) : ''}
              </div>
            </form> :
            // if results are grouped, display the Loading page
            // else, results are separate and display the JobsList cards page
            (!uploading?(!groupresults?
              <Redirect to='/results' />:
              <Loading jobId={this.state.jobId} />
            ):"")
          }
        </div>
      )
    }
  }

  Subtyping = connect()(Subtyping)

  export default Subtyping


The important part to note is the form submission:

.. code-block:: jsx

  axios.post(API_ROOT + 'upload', data, createConfig(this._updateUploadProgress))
        .then(response => {
          console.log(response)
          // no longer uploading
          this.setState({
            uploading: false
          })
          let jobs = response.data
          // handle the return
          for(let job in jobs){
            let f = (this.state.file.length > 1 ?
            String(this.state.file.length + ' Files')
            :this.state.file[0].name)
            if(jobs[job].analysis === "Antimicrobial Resistance"){
              this.props.dispatch(addJob(job,
                "Antimicrobial Resistance",
                new Date().toLocaleTimeString(),
                subtypingDescription(f, this.state.pi, false, false, this.state.amr)
              ))

(truncated)

We can take a look at a simpler example in `Fishers.js`_ where there aren't multiple `jobs[job].analysis === "Antimicrobial Resistance"` analysis types in a single form.

.. code-block:: jsx

  axios.post(API_ROOT + 'newgroupcomparison', {
        groups: groups,
        target: target
      })
        .then(response => {
          console.log(response);
          const jobId = response.data;
          const hasResult = true;
          this.setState({jobId})
          this.setState({hasResult})
          // add jobid to redux store
          this.props.dispatch(addJob(jobId,
            'fishers',
            new Date().toLocaleTimeString(),
            fishersDescription(groups, target)
          ))
        });

First you'd want to change the POST route so it targets your new endpoint.

.. code-block:: jsx

  axios.post(API_ROOT + 'someroute', {

Note that `API_ROOT` prepends the `api/v0/` so the full route might be `api/v0/someroute`.

Now we need to dispatch an `addJob` action to Redux. This stores the job information in our Redux store, under the `jobs` list. In our example, we used a function to generate the description, but if you were to add a dispatch for your `ml` module you might do something like:

.. code-block:: jsx

  axios.post(API_ROOT + 'someroute', {
          groups: groups,
          target: target
        })
          .then(response => {
            console.log(response);
            const jobId = response.data;
            const hasResult = true;
            this.setState({jobId})
            this.setState({hasResult})
            // add jobid to redux store
            this.props.dispatch(addJob(jobId,
              'ml',
              new Date().toLocaleTimeString(),
              'my description of what ml options were chosen'
            ))
          });

Then, after creating your form, in `/src/containers/App.js`_ add an import for your container:

.. code-block:: jsx

  import ML from '../containers/ML'

then add a route:

.. code-block:: jsx

   <Switch key={location.key}>
      <Route exact path="/" location={location} component={Home} />
      <Route path="/fishers" location={location} component={Fishers} />
      <Route path="/subtyping" location={location} component={Subtyping} />
      <Route exact path="/results" location={location} component={Results} />
      <Route path="/results/:hash" location={location} component={VisibleResult} />
    </Switch>

would become:

.. code-block:: jsx

   <Switch key={location.key}>
      <Route exact path="/" location={location} component={Home} />
      <Route path="/fishers" location={location} component={Fishers} />
      <Route path="/subtyping" location={location} component={Subtyping} />
      <Route path="/ml" location={location} component={ML} />
      <Route exact path="/results" location={location} component={Results} />
      <Route path="/results/:hash" location={location} component={VisibleResult} />
    </Switch>

Now your form will render at `/ml`.

Adding a Results Page
---------------------

When your form dispatches an `addJob` action to Redux, the `/results` page will automatically populate and poll for the status of your job. You'll now need to add a component to display the results to the user. For tabular results, we use the `react-bootstrap-table`_ package. You can look at `/src/components/ResultsFishers.js`_ as a starting point.

.. _`react-bootstrap-table`: https://github.com/AllenFang/react-bootstrap-table

.. code-block:: jsx

  import React, { Component } from 'react';
  import { connect } from 'react-refetch'
  // progress bar
  import CircularProgress from 'react-md/lib/Progress/CircularProgress';
  // requests
  import { API_ROOT } from '../middleware/api'
  // Table
  import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

  class ResultFishers extends Component {
    render() {
      const { results } = this.props
      const options = {
        searchPosition: 'left'
      };
      if (results.pending){
        return <div>Waiting for server response...<CircularProgress key="progress" id='contentLoadingProgress' /></div>
      } else if (results.rejected){
        return <div>Couldn't retrieve job: {this.props.jobId}</div>
      } else if (results.fulfilled){
        console.log(results)
        return (
          <BootstrapTable data={results.value.data} exportCSV search options={options}>
            <TableHeaderColumn  isKey dataField='0' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='400' csvHeader='Target'>Target</TableHeaderColumn>
            <TableHeaderColumn  dataField='1' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } csvHeader='QueryA'>QueryA</TableHeaderColumn>
            <TableHeaderColumn  dataField='2' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } csvHeader='QueryB'>QueryB</TableHeaderColumn>
            <TableHeaderColumn  dataField='3' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='#Present QueryA'>#Present QueryA</TableHeaderColumn>
            <TableHeaderColumn  dataField='4' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='#Absent QueryA'>#Absent QueryA</TableHeaderColumn>
            <TableHeaderColumn  dataField='5' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='#Present QueryB'>#Present QueryB</TableHeaderColumn>
            <TableHeaderColumn  dataField='6' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='#Absent QueryB'>#Absent QueryB</TableHeaderColumn>
            <TableHeaderColumn  dataField='7' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='P-Value'>P-Value</TableHeaderColumn>
            <TableHeaderColumn  dataField='8' dataSort filter={ { type: 'TextFilter', placeholder: 'Please enter a value' } } width='140' csvHeader='Odds Ratio'>Odds Ratio</TableHeaderColumn>
          </BootstrapTable>
        );
      }
    }
  }

  export default connect(props => ({
    results: {url: API_ROOT + `results/${props.jobId}`}
  }))(ResultFishers)

In the case of Fisher's, the response from Flask is generated by the:

.. code-block:: python

  df.to_json(orient='split')

from the Pandas DataFrame. This creates an object with keys `columns`, `data`, and `index`. In particular, under the `data` key is an array of arrays:

.. code-block:: jsx

  [["https:\/\/www.github.com\/superphy#hlyC","O111","O24",1.0,0.0,0.0,1.0,null,1.0],["https:\/\/www.github.com\/superphy#hlyB","O111","O24",1.0,0.0,0.0,1.0,null,1.0],["https:\/\/www.github.com\/superphy#hlyA","O111","O24",1.0,0.0,0.0,1.0,null,1.0]]

(only an example, the full results.value.data array is 387 arrays long, and can vary)

Note that we use

.. code-block:: jsx

  dataField='5'

for example, which we apply to:

.. code-block:: jsx

  csvHeader='#Present QueryB'

which is used for exporting to .csv. And in between the TableHeaderColumn tags:

.. code-block:: jsx

  <TableHeaderColumn>#Present QueryB</TableHeaderColumn>

(options removed)

The `#Present QueryB` is used when displaying the webpage.

Finally, in `/src/components/ResultsTemplates.js`_ import you component:

.. code-block:: jsx

  import ResultML from './ResultML'

and add the case to the switch which decides which result view to return:

.. code-block:: javascript

  case "ml":
      return <ML jobId={job.hash} />

.. _`reactapp`: https://github.com/superphy/reactapp
.. _`supervisord-rq.conf`: https://github.com/superphy/backend/blob/master/app/supervisord-rq.conf
.. _`install node`: https://nodejs.org/en/
.. _`install yarn`: https://yarnpkg.com/en/docs/install#mac-tab
.. _`api.js`: https://github.com/superphy/reactapp/blob/master/src/middleware/api.js
.. _`Fishers.js`: https://github.com/superphy/reactapp/blob/master/src/containers/Fishers.js
.. _`Subtyping.js`: https://github.com/superphy/reactapp/blob/master/src/containers/Subtyping.js
.. _`/src/containers/App.js`: https://github.com/superphy/reactapp/blob/master/src/containers/App.js
.. _`/src/components/ResultsFishers.js`: https://github.com/superphy/reactapp/blob/master/src/components/ResultFishers.js
.. _`/src/components/ResultsTemplates.js`: https://github.com/superphy/reactapp/blob/master/src/components/ResultsTemplates.js

Packaging It All Together
=========================

Once the main `superphy/backend` repo has any submodule you specified at the correct head, you can rebuild the entire composition by running:

.. code-block:: sh

  git submodule update
  docker-compose build --no-cache .
  docker-compose up

Alternatively, to run docker-compose in detached-head mode (where the composition runs entirely by the Docker daemon, without need for a linked shell), run:

.. code-block:: sh

  docker-compose up -d

Adding a New Option to the Subtyping Module
===========================================

While reviewing `Adding a New Module`_ is important to see the general workflow, if you're modifying the Subtyping task to add a new analysis option you'll have to *modify* the existing codebase instead of simply *adding* a new module. There are a few things you'll have to do:

1. Add a Switch to the `Subtyping.js`_ and ensure the selection is appended to the formData
2. Handle the selected option in the ``upload()`` function in `ra_posts.py`_
3. Create an enqueue() call in `spfy.py`_
4. Create a folder or git submodule in ``app/modules`` which contains the rest of the code your option needs
5. If you want to return the results to the front-end or upload the results to blazegraph, you'll have to parse your return to fit the format of `datastruct_savvy.py`_ and then enqueue the datastruct_savvy() call with your results as the arg and all that job to the ``jobs`` dict in ``upload()`` of `ra_posts.py`
6. Then we need to edit `beautify.py`_ to parse the same dict used for `datastruct_savvy.py`_. Afterwhich, the ``merge_job_results()`` in `ra_statuses.py`_ will automatically merge the result and return it to the front-end

.. _`Subtyping.js`: https://github.com/superphy/reactapp/blob/master/src/containers/Subtyping.js
.. _`ra_posts.py`: https://github.com/superphy/backend/blob/master/app/routes/ra_posts.py
.. _`datastruct_savvy.py`: https://github.com/superphy/backend/blob/master/app/modules/turtleGrapher/datastruct_savvy.py
.. _`ra_statuses.py`: https://github.com/superphy/backend/blob/master/app/routes/ra_statuses.py
.. _`spfy.py`: https://github.com/superphy/backend/blob/master/app/modules/spfy.py
.. _`beautify.py`: https://github.com/superphy/backend/blob/master/app/modules/beautify/beautify.py

Adding a Checkbox to the Subtyping.js
-----------------------------------

As shown in `Subtyping.js`_ , checkboxes are defined like so:

.. code-block:: jsx

  <Checkbox
    id="serotype"
    name="check serotype"
    checked={serotype}
    onChange={this._updateSerotype}
    label="Serotype"
  />

The important points are the ``checked={serotype}`` where ``serotype`` refers to a state defined by:

.. code-block:: jsx

  constructor(props) {
    super(props);
    this.state = {
      file: null,
      pi: 90,
      amr: false,
      serotype: true,
      vf: true,
      submitted: false,
      open: false,
      msg: '',
      jobId: "",
      hasResult: false,
      groupresults: true,
      bulk: false,
      progress: 0
    }
  }

and uses the ``onChange`` function:

.. code-block:: jsx

  _updateSerotype = (value) => {
    this.setState({ serotype: value })
  }

which is appended to the form by:

.. code-block:: jsx

  data.append('options.serotype', this.state.serotype)

So if you wanted to add a new option, say ``Phylotyper``, you'd create a checkbox like so:

.. code-block:: jsx

  <Checkbox
    id="phylotyper"
    name="check phylotyper"
    checked={phylotyper}
    onChange={this._updatePhylotyper}
    label="Use Phylotyper"
  />

and add the default state as true in the constructor:

.. code-block:: jsx

  phylotyper: true

with the corresponding ``onChange`` function:

.. code-block:: jsx

  _updatePhylotyper = (value) => {
    this.setState({ phylotyper: value })
  }

which is appended to the form by:

.. code-block:: jsx

  data.append('options.phylotyper', this.state.phylotyper)

and that's it for the form part!

Handling a New Option in ra_posts.py
------------------------------------

Looking at the function definition, we can see that ``upload()`` in `ra_posts.py`_ is the route we want to edit:

.. code-block:: python

  # for Subtyping module
  # the /api/v0 prefix is set to allow CORS for any postfix
  # this is a modification of the old upload() methods in views.py
  @bp_ra_posts.route('/api/v0/upload', methods=['POST'])
  def upload():

We store user-selected options in the ``options`` dictionary defined at the beginning, with a slight exception in the ``pi`` option due to legacy reasons. For example, the ``serotype`` is defined via:

.. code-block:: python

  options['serotype']=True

So let's define the default for phylotyper to be true:

.. code-block:: python

  options['phylotyper']=True

Then we need to process the formdata. The following code block is used to convert the lower-case ``false`` is javascript to the upper case ``False`` in python, likewise with ``true``:

.. code-block:: python

  # processing form data
  for key, value in form.items():
      #we need to convert lower-case true/false in js to upper case in python
          #remember, we also have numbers
      if not value.isdigit():
          if value.lower() == 'false':
              value = False
          else:
              value = True
          if key == 'options.amr':
              options['amr']=value
          if key == 'options.vf':
              options['vf']=value
          if key == 'options.serotype':
              options['serotype']=value
          if key == 'options.groupresults':
              groupresults = value
          if key == 'options.bulk':
              options['bulk'] = value
      else:
          if key =='options.pi':
              options['pi']=int(value)

So for ``phylotyper``, we'll add an ``if`` block:

.. code-block:: python

  if key == 'options.phylotyper':
    options['phylotyper']=value

After this point, your option will be passed to the `spfy.py`_ call.

Create an enqueue() Call in spfy.py
-----------------------------------

.. warning:: A previous version of the docs recommended you create your own module (adjacent to `spfy.py`_) to enqueue your option. Note that this is no longer recommended as you have to support the bulk uploading and the backlog option in the `Subtyping.js`_ card.

Currently, we define pipelines denoted within comment blocks:

.. code-block:: python

  # AMR PIPELINE
  def amr_pipeline(multiples):
      job_amr = multiples.enqueue(amr, query_file, depends_on=job_id)
      job_amr_dict = multiples.enqueue(
          amr_to_dict, query_file + '_rgi.tsv', depends_on=job_amr)
      # this uploads result to blazegraph
      if single_dict['options']['bulk']:
          job_amr_datastruct = multiples.enqueue(
              datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict, result_ttl=-1)
      else:
          job_amr_datastruct = multiples.enqueue(
              datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict)
      d = {'job_amr': job_amr, 'job_amr_dict': job_amr_dict,
           'job_amr_datastruct': job_amr_datastruct}
      # we still check for the user-selected amr option again because
      # if it was not selected but BACKLOG_ENABLED=True, we dont have to
      # enqueue it to backlog_multiples_q since beautify doesnt upload
      # blazegraph
      if single_dict['options']['amr'] and not single_dict['options']['bulk']:
          job_amr_beautify = multiples.enqueue(
              beautify, single_dict, query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict, result_ttl=-1)
          d.update({'job_amr_beautify': job_amr_beautify})
      return d

  if single_dict['options']['amr']:
      amr_jobs = amr_pipeline(multiples_q)
      job_amr = amr_jobs['job_amr']
      job_amr_dict = amr_jobs['job_amr_dict']
      job_amr_datastruct = amr_jobs['job_amr_datastruct']
      if not single_dict['options']['bulk']:
          job_amr_beautify = amr_jobs['job_amr_beautify']
  elif config.BACKLOG_ENABLED:
      amr_pipeline(backlog_multiples_q)
  # END AMR PIPELINE

The ``AMR PIPELINE`` is a good reference point to start from. Note the relative imports to `app/` in `spfy.py`:

.. code-block:: python

  from modules.amr.amr import amr

In this case, there is an folder called ``amr`` with module ``amr`` and main method ``amr``. You don't have to follow the same naming structure of course.

A simple definition for ``phylotyper`` might start like so:

.. code-block:: python

  def blob_savvy_enqueue(single_dict):
    # ...
    # PHYLOTYPER PIPEINE
    def phylotyper_pipeline(singles):
      # the main enqueue call
      job_phylotyper = singles.enqueue(phylotyper_main, query_file, depends_on=job_id)
      d.update('job_phylotyper': job_phylotyper)
      return d

    # check if the phylotyper option was selected by the user
    if single_dict['options']['phylotyper']:
      phylotyper_jobs = phylotyper_pipeline(singles_q)
      job_phylotyper = phylotyper_jobs['job_phylotyper']
    elif config.BACKLOG_ENABLED:
      phylotyper_pipeline(backlog_singles_q)

.. note:: the ``singles``-type queues are used when the enqueued module can't be run in parallel on the same machine (eg. you cant open up two terminals and run the module at the same time). If the module you're adding can be run in parrallel, you can replace the ``singles`` queues with the ``multiples`` queues.

The way enqueue() works is that the first *args is the function to enqueue and the following *args are for the function itself. ``depends_on`` alows us to specify a job in RQ that must be completed prior to your function.

The code above is just a start and doesn't support the bulk uploading option, storing of results in blazegraph, or return to the front-end. In this case, the inner `phylotyper_pipeline()` function is used to enqueue the task. We do this to support the bulk uploading option: in the regular case where the user has selected the phylotyper option, we call the pipeline method with the ``singles_q`` which always runs before tasks in any ``backlog_*`` queue (See `Optional: Adding a new Queue`_ for how this is implemented). Now, if the user have enabled backlog tasks, where all tasks are run even if the user doesn't select them, then phylotyper_pipeline() is still called except:

1. We call the pipeline with the backlog queue
2. We don't care to store any job data

The additional functions: ``amr_to_dict`` converts the amr results into the structure required by ``datastruct_savvy``. The following code-block is used to enable bulk uploading. Note that if bulk uploading is selected, we set a ``result_ttl=-1`` for the status checking functions in `ra_statuses.py`_ to use for checking completion.

.. note:: This ``result_ttl=-1`` requirement will no longer be necessary when job dependency checking is streamlined in release candidate v5.0.0

.. code-block:: python

  # this uploads result to blazegraph
  if single_dict['options']['bulk']:
      job_amr_datastruct = multiples.enqueue(
          datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict, result_ttl=-1)
  else:
      job_amr_datastruct = multiples.enqueue(
          datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict)

The ``beautify`` function is used to convert the return of ``amr_to_dict`` to the format required by the front-end React application. It is only enqueued if the ``amr`` option, for example, was selected but bulk uploading was not selected.

.. _`ra_statuses.py`: https://github.com/superphy/backend/blob/master/app/routes/ra_statuses.py

Adding a Git Submodule
----------------------

.. warning:: RQ enqueus functions relative to being inside the ``app/`` folder, depending on your code base you may have to refactor.

The process to add a submodule for an option in the Subtyping card is the same as in `Integrating your Codebase into Spfy`_. Please refer to that sectio for details.

Pickling the Result of Intermediate Tasks
-----------------------------------------

We handle parsing of intermediate results by pickling the python object and storing it in the same location as the genome file. For example, `amr_to_dict.py`_ handles this by:

.. code-block:: python

  p = os.path.join(amr_file + '_rgi.p')
  pickle.dump(amr_dict, open(p, 'wb'))

If you need to store results between tasks, do so in the same manner.

.. note:: A cleanup task will be added in release candidate v5.0.0 which wipes the temporary containing folder once all jobs are complete, so you don't have to worry about cleanup for now.

Modifying your Return to Fit datastruct_savvy.py
------------------------------------------------

`datastruct_savvy.py`_ expects the format of modules which return gene hits (ex. Virulence Factors or Antimicrobial Resistance Genes) to have the form (an example of the conversion can be found in `amr_to_dict.py`_:

.. code-block:: python

  {'Antimicrobial Resistance':
    {'somecontigid1':{'START':1, 'STOP':2, 'GENE_NAME': 'somename', 'ORIENTATION':'+', 'CUT_OFF':90},
    'somecontigid2':{'START':1, 'STOP':2, 'GENE_NAME': 'somename', 'ORIENTATION':'+', 'CUT_OFF':90},
    'somecontigid3':{'START':1, 'STOP':2, 'GENE_NAME': 'somename', 'ORIENTATION':'+', 'CUT_OFF':90}
  }}

and expects the result of serotyping as:

  {'Serotype':
    {'O-Type':'O1',
    'H-Type':'H2',}
  }

If you were adding a return similar to ``serotype``, such as with phylotyper, define a parsing function in `datastruct_savvy.py`_ similar to ``parse_serotype()``:

.. code-block:: python

  def parse_serotype(graph, serotyper_dict, uriIsolate):
    if 'O type' in serotyper_dict:
        graph.add((uriIsolate, gu('ge:0001076'),
                   Literal(serotyper_dict['O type'])))
    if 'H type' in serotyper_dict:
        graph.add((uriIsolate, gu('ge:0001077'),
                   Literal(serotyper_dict['H type'])))
    if 'K type' in serotyper_dict:
        graph.add((uriIsolate, gu('ge:0001684'),
                   Literal(serotyper_dict['K type'])))

    return graph

Then add the call in the elif in ``generate_datastruct()``:

.. code-block:: python

  # graphing functions
  for key in results_dict.keys():
      if key == 'Serotype':
          graph = parse_serotype(graph,results_dict['Serotype'],uriIsolate)
      elif key == 'Virulence Factors':
          graph = parse_gene_dict(graph, results_dict['Virulence Factors'], uriGenome, 'VirulenceFactor')
      elif key == 'Antimicrobial Resistance':
          graph = parse_gene_dict(graph, results_dict['Antimicrobial Resistance'], uriGenome, 'AntimicrobialResistanceGene')
  return graph

If you're adding an option that returns specific hits, such as PanSeq, parse to results as before and call ``parse_gene_dict()`` on it.

.. code-block:: python

  # graphing functions
  for key in results_dict.keys():
      if key == 'Serotype':
          graph = parse_serotype(graph,results_dict['Serotype'],uriIsolate)
      elif key == 'Virulence Factors':
          graph = parse_gene_dict(graph, results_dict['Virulence Factors'], uriGenome, 'VirulenceFactor')
      elif key == 'Antimicrobial Resistance':
          graph = parse_gene_dict(graph, results_dict['Antimicrobial Resistance'], uriGenome, 'AntimicrobialResistanceGene')
      elif key == 'Panseq':
          graph = parse_gene_dict(graph, results_dict['Panseq'], uriGenome, 'PanseqRegion')
  return graph

.. _`datastruct_savvy.py`: https://github.com/superphy/backend/blob/master/app/modules/turtleGrapher/datastruct_savvy.py
.. _`amr_to_dict.py`: https://github.com/superphy/backend/blob/master/app/modules/amr/amr_to_dict.py

You'll then have to enqueue the ``datastruct_savvy()`` call in `spfy.py`_ similar to:

.. code-block:: python

  # this uploads result to blazegraph
  if single_dict['options']['bulk']:
      job_amr_datastruct = multiples.enqueue(
          datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict, result_ttl=-1)
  else:
      job_amr_datastruct = multiples.enqueue(
          datastruct_savvy, query_file, query_file + '_id.txt', query_file + '_rgi.tsv_rgi.p', depends_on=job_amr_dict)

Then the datastruct result is added to the `d` dictionary of your inner pipeline function:

.. code-block:: python

  d = {'job_amr': job_amr, 'job_amr_dict': job_amr_dict,
       'job_amr_datastruct': job_amr_datastruct}

and, outside of the inner function, it's assigned as ``job_amr_datastruct``:

.. code-block:: python

  job_amr_datastruct = amr_jobs['job_amr_datastruct']

By default, we set the datastruct as the end task to send back - this is to faciliate bulk uploading. If the user-doesn't select the bulk option, then the return is the result from ``beautify()``:

.. code-block:: python

  # new to 4.3.3 if bulk ids used return the endpoint of datastruct generation
  # to poll for completion of all jobs
  # these two ifs handle the case where amr (or vf or serotype) might not
  # be selected but bulk is
  if (single_dict['options']['vf'] or single_dict['options']['serotype']):
      ret_job_ectyper = job_ectyper_datastruct
  if single_dict['options']['amr']:
      ret_job_amr = job_amr_datastruct
  # if bulk uploading isnt used, return the beautify result as the final task
  if not single_dict['options']['bulk']:
      if (single_dict['options']['vf'] or single_dict['options']['serotype']):
          ret_job_ectyper = job_ectyper_beautify
      if single_dict['options']['amr']:
          ret_job_amr = job_amr_beautify
  # add the jobs to the return
  if (single_dict['options']['vf'] or single_dict['options']['serotype']):
      jobs[ret_job_ectyper.get_id()] = {'file': single_dict[
          'i'], 'analysis': 'Virulence Factors and Serotype'}
  if single_dict['options']['amr']:
      jobs[ret_job_amr.get_id()] = {'file': single_dict[
          'i'], 'analysis': 'Antimicrobial Resistance'}

Modifying beautify.py
---------------------

Technically, you'll mostly be using the ``json_return()`` method from `beautify.py`_ as it performs the core conversion to json. ``beautify()`` also performs a number of checks that are specific to ECTyper and RGI: namely, we parse the ``gene_dict`` and find the widest hit in a given contig. For new modules, we recommand you just create a basic function in `beautify.py`_ to perform the ``pickle.load()`` to bypass the widest_hit search and failed handling. For example:

.. code-block:: python

  def beautify_myoption(args_dict, pickled_dictionary):
    gene_dict = pickle.load(open(pickled_dictionary, 'rb'))
    # this converts our dictionary structure into json and adds metadata (filename, etc.)
    json_r =  json_return(args_dict, gene_dict)
    return json_r

If you're adding a serotyping tool such as ``phylotyper``, modifying:

.. code-block:: python

  if analysis == 'Serotype':

to be:

.. code-block:: python

  if analysis in ('Serotype','Phylotyper'):

should be all the modification to ``json_return()`` that is required.

For results similar to VF/AMR, where we have a list of genes, you can call ``json_return()`` directly without modification.

With `beautify.py`_ modified, add the ``beautify_myoption()`` call to your pipeline like so:

.. code-block:: python

  if single_dict['options']['phylotyper'] and not single_dict['options']['bulk']:
    job_phylotyper_beautify = multiples.enqueue(
        beautify_myoption, single_dict, query_file + '_phylotyper.p', depends_on=job_phylotyper_dict, result_ttl=-1)
    d.update({'job_phylotyper_beautify': job_phylotyper_beautify})

and then set the result as the return to the front-end:

.. code-block:: python

  # if bulk uploading isnt used, return the beautify result as the final task
  if not single_dict['options']['bulk']:
      if (single_dict['options']['vf'] or single_dict['options']['serotype']):
          ret_job_ectyper = job_ectyper_beautify
      if single_dict['options']['amr']:
          ret_job_amr = job_amr_beautify

Debugging
=========

You can see all the containers on your host computer by running:

.. code-block:: sh

  docker ps

When running commands within ``/backend`` (at the same location as the ``docker-compose.yml`` file), you can see the composition-specific containers by running:

.. code-block:: sh

  docker-compose logs

Within the repo, you can also see logs for specific containers by referencing the service name, as defined in the ``docker-compose.yml`` file. For example, logs for the Flask webserver can be retrieved by running:

.. code-block:: sh

  docker-compose logs webserver

or if you wanted the tail:

.. code-block:: sh

  docker-compose logs --tail=100 webserver

or for Blazegraph:

.. code-block:: sh

  docker-compose logs blazegraph

To clean up after Docker, see the excellent Digital Ocean guide on `How To Remove Docker Images, Containers, and Volumes`_.

.. _`How To Remove Docker Images, Containers, and Volumes`: https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

Monitoring Flask
----------------

Three options:

1. Docker captures all `stdout` messages into Docker's logs. You can see them by running:

  .. code-block:: sh

    docker logs backend_webserver_1

2. Flask is also configured to report errors via Sentry; copy your DSN key and uncomment the ``SENTRY_DSN`` option in ``/app/config.py``.

3. Drop a shell info the webserver container, then you can run explore the file structure from there. The webserver will typically run as ``backend_webserver_1``. Note that there won't be any ``access.log`` or similar as this information is collected through Docker's logs.

Monitoring RQ
-------------

To monitor the status of RQ tasks and check on failed jobs, you have two options:

1. Setup a https://sentry.io account and copy your DSN into
   ``/app/config.py``
2. Port 9181 is mapped to host on Service ``backend-rq``, you can use
   ``rq-dashboard`` via:

  1. ``docker exec -it backend_worker_1 sh`` this drops a shell into the
     rq worker container which has rq-dashboard installed via conda
  2. ``rq-dashboard -H redis`` runs rq-dashboard and specifies the *redis*
     host automatically defined by docker-compose
  3. then on your host machine visit http://localhost:9181

We recommend using ``RQ-dashboard`` to see jobs being enqueued live when testing as ``Sentry`` only reports failed jobs. On remote deployments, we use ``Sentry`` for error reporting.

.. warning:: ``RQ-dashboard`` will not report errors from the Flask webserver. In addition, jobs enqueued with ``depends_on`` will not appear on the queues list until their dependencies are complete.

Debugging Javascript
--------------------

For testing simple commands, I use the Node interpreter similar to how one might use Python's interpreter:

.. code-block:: sh

  node
  .exit

We use the Chrome extension `React Dev Tools`_ to see our components and state, as defined in React; Chrome's DevTools will list ``Elements`` in their HTML form which, while not particularly useful to debug React-specific code, can be used to check which CSS stylings are applied.

The `Redux Dev Tools`_ extension is used to monitor the state of our reactapp's Redux store. This is useful to see that your ``jobs`` are added correctly.

Finally, if you clone our `reactapp`_ repo, and run:

.. code-block:: sh

  yarn start

any saved changes will be linted with ``eslint``.

Editing the Docs
================

Setup
-----

.. code-block:: sh

  cd docs/
  sphinx-autobuild source _build_html

Then you can visit http://localhost:8000 to see you changes live. Note that it uses the default python theme locally, and the default readthedocs theme when pushed.
