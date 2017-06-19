===============
Developer Guide
===============

.. contents:: Table of Contents
   :local:

Getting Started
===============

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
genome files in total.

.. _`old github/semantic repo`: https://raw.githubusercontent.com/superphy/semantic/master/superphy/src/upload/python/data/download_files.txt

Docker Caveats
--------------

We've had problems with Ubuntu Desktop versions 16.04.2 LTS and 17.04 not connecting to NPM when building Docker images and from within the building. Builds work fine with Ubuntu Server 16.04.2 LTS on Cybera and for Ubuntu Server 12.04 or 14.04 LTS on Travis-CI. Within the building, RHEL-based operating systems (CentOS / Scientific Linux) build our NPM-dependent images (namely, `reactapp`_) just fine.

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
