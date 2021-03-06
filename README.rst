.. tag:intro-begin

|Build Status| |GitHub license| |Docs|

**Spfy**: Platform for predicting subtypes from E.coli whole genome sequences, and builds graph data for population-wide comparative analyses.

Published as: Le,K.K., Whiteside,M.D., Hopkins,J.E., Gannon,V.P.J., Laing,C.R. Spfy: an integrated graph database for real-time prediction of bacterial phenotypes and downstream comparative analyses. Database (2018) Vol. 2018: article ID bay086; doi:10.1093/database/bay086

Live: https://lfz.corefacility.ca/superphy/spfy/

.. image:: screenshots/screen-results_list.png
    :align: center
    :alt: screenshot of the results page

Use:
----

1. Install Docker (& Docker-Compose separately if you're on Linux,
   `link <https://docs.docker.com/compose/install/>`__). mac/windows
   users have Compose bundled with Docker Engine.
2. ``git clone --recursive https://github.com/superphy/spfy.git``
3. ``cd spfy/``
4. ``docker-compose up``
5. Visit http://localhost:8090
6. Eat cake :cake:

Submodule Build Statuses:
-------------------------

ECTyper:

.. image:: https://travis-ci.org/phac-nml/ecoli_serotyping.svg?branch=superphy
    :target: https://travis-ci.org/phac-nml/ecoli_serotyping

PanPredic:

.. image:: https://travis-ci.org/superphy/PanPredic.svg?branch=master
    :target: https://travis-ci.org/superphy/PanPredic

Docker Image for Conda:

.. image:: https://travis-ci.org/superphy/docker-flask-conda.svg?branch=master
    :target: https://travis-ci.org/superphy/docker-flask-conda

Stats:
------

Comparing different population groups:

|fo|

.. |fg| image:: screenshots/fishers_genomes.png
    :width: 20%
    :alt: As a factor of # Genomes per Target

.. |ft| image:: screenshots/fishers_targets.png
    :width: 20%
    :alt: As a factor of # Targets Retrieved per Genome

.. |fo| image:: screenshots/fishers_overall.png
    :width: 20%
    :alt: Overall Performance

Runtimes of subtyping modules:

.. image:: screenshots/spfy_indivs.png
    :width: 20%
    :alt: Runtimes of individual analyses

CLI: Generate Graph Files:
--------------------------

-  If you wish to only create rdf graphs (serialized as turtle files):

1. First install miniconda and activate the environment from
   https://raw.githubusercontent.com/superphy/docker-flask-conda/master/app/environment.yml
2. cd into the app folder (where RQ workers typically run from):
   ``cd app/``
3. Run savvy.py like so:
   ``python -m modules/savvy -i tests/ecoli/GCA_001894495.1_ASM189449v1_genomic.fna``
   where the argument after the ``-i`` is your genome (FASTA) file.

CLI: Generate Ontology:
-----------------------
.. image:: screenshots/ontology.png
    :align: center
    :alt: screenshot of the results page

The ontology for Spfy is available at:
https://raw.githubusercontent.com/superphy/backend/master/app/scripts/spfy\_ontology.ttl
It was generated using
https://raw.githubusercontent.com/superphy/backend/master/app/scripts/generate\_ontology.py
with shared functions from Spfy's backend code. If you wish to run it,
do: 1. ``cd app/`` 2. ``python -m scripts/generate_ontology`` which will
put the ontology in ``app/``

You can generate a pretty diagram from the .ttl file using http://www.visualdataweb.de/webvowl/

CLI: Enqueue Subtyping Tasks w/o Reactapp:
------------------------------------------

.. note:: currently setup for just .fna files

You can bypass the front-end website and still enqueue subtyping jobs by:

1. First, mount the host directory with all your genome files to ``/datastore`` in the containers.

  For example, if you keep your files at ``/home/bob/ecoli-genomes/``, you'd
  edit the ``docker-compose.yml`` file and replace:

  .. code-block:: yaml

    volumes:
    - /datastore

  with:

  .. code-block:: yaml

    volumes:
    - /home/bob/ecoli-genomes:/datastore

2. Then take down your docker composition (if it's up) and restart it

  .. code-block:: shell

    docker-compose down
    docker-compose up -d

3. Drop and shell into your webserver container (though the worker containers would work too) and run the script.

  .. code-block:: shell

    docker exec -it backend_webserver_1 sh
    python -m scripts/sideload
    exit

Note that reisdues may be created in your genome folder.

Architecture:
-------------
.. image:: screenshots/docker.svg
    :align: center
    :alt: screenshot of the results page

+------+------+------+------+
| Dock | Port | Name | Des  |
| er   | s    | s    | crip |
| Imag |      |      | tion |
| e    |      |      |      |
+======+======+======+======+
| back | 80/t | back | the  |
| end- | cp,  | end\ | main |
| rq   | 443/ | _wor | redi |
|      | tcp  | ker\ | s    |
|      |      | _1   | queu |
|      |      |      | e    |
|      |      |      | work |
|      |      |      | ers  |
+------+------+------+------+
| back | 80/t | back | this |
| end- | cp,  | end\ | hand |
| rq-b | 443/ | _wor | les  |
| laze | tcp  | ker- | spfy |
| grap |      | blaz | ID   |
| h    |      | egra | gene |
|      |      | ph-i | rati |
|      |      | ds\_ | on   |
|      |      | 1    | for  |
|      |      |      | the  |
|      |      |      | blaz |
|      |      |      | egra |
|      |      |      | ph   |
|      |      |      | data |
|      |      |      | base |
+------+------+------+------+
| back | 0.0. | back | the  |
| end  | 0.0: | end\ | flas |
|      | 8000 | _web | k    |
|      | ->80 | -ngi | back |
|      | /tcp | nx-u | end  |
|      | ,    | wsgi | whic |
|      | 443/ | \_1  | h    |
|      | tcp  |      | hand |
|      |      |      | les  |
|      |      |      | enqu |
|      |      |      | euei |
|      |      |      | ng   |
|      |      |      | task |
|      |      |      | s    |
+------+------+------+------+
| supe | 0.0. | back | Blaz |
| rphy | 0.0: | end\ | egra |
| /bla | 8080 | _bla | ph   |
| zegr | ->80 | zegr | Data |
| aph: | 80/t | aph\ | base |
| 2.1. | cp   | _1   |      |
| 4-in |      |      |      |
| fere |      |      |      |
| ncin |      |      |      |
| g    |      |      |      |
+------+------+------+------+
| redi | 6379 | back | Redi |
| s:3. | /tcp | end\ | s    |
| 2    |      | _red | Data |
|      |      | is\_ | base |
|      |      | 1    |      |
+------+------+------+------+
| reac | 0.0. | back | fron |
| tapp | 0.0: | end\ | t-en |
|      | 8090 | _rea | d    |
|      | ->50 | ctap | to   |
|      | 00/t | p\_1 | spfy |
|      | cp   |      |      |
+------+------+------+------+

Further Details:
----------------

The ``superphy/backend-rq:2.0.0`` image is *scalable*: you can create as
many instances as you need/have processing power for. The image is
responsible for listening to the ``multiples`` queue (12 workers) which
handles most of the tasks, including ``RGI`` calls. It also listens to
the ``singles`` queue (1 worker) which runs ``ECTyper``. This is done as
``RGI`` is the slowest part of the equation. Worker management in
handled in ``supervisor``.

The ``superphy/backend-rq-blazegraph:2.0.0`` image is not scalable: it
is responsible for querying the Blazegraph database for duplicate
entries and for assigning spfyIDs in *sequential* order. It's functions
are kept as minimal as possible to improve performance (as ID generation
is the one bottleneck in otherwise parallel pipelines); comparisons are
done by sha1 hashes of the submitted files and non-duplicates have their
IDs reserved by linking the generated spfyID to the file hash. Worker
management in handled in ``supervisor``.

The ``superphy/backend:2.0.0`` which runs the Flask endpoints uses
``supervisor`` to manage inner processes: ``nginx``, ``uWsgi``.

Blazegraph:
-----------

-  We are currently running Blazegraph version 2.1.4. If you want to run
   Blazegraph separately, please use the same version otherwise there
   may be problems in endpoint urls / returns (namely version 2.1.1).
   See `#63 <https://github.com/superphy/backend/issues/63>`__
   Alternatively, modify the endpoint accordingly under
   ``database['blazegraph_url']`` in ``/app/config.py``

Contributing:
-------------

Steps required to add new modules are documented in the `Developer Guide`_.

.. _`Developer Guide`: http://superphy.readthedocs.io/en/latest/contributing.html

.. |Build Status| image:: https://travis-ci.org/superphy/spfy.svg?branch=master
   :target: https://travis-ci.org/superphy/spfy
.. |GitHub license| image:: https://img.shields.io/badge/license-Apache%202-blue.svg
   :target: https://raw.githubusercontent.com/superphy/spfy/master/LICENSE
.. |Docs| image:: https://readthedocs.org/projects/spfy/badge/?version=latest
   :target: http://spfy.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. tag:intro-end
