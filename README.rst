|Build Status| |GitHub license|

**Spfy**: speedy `superphy <https://github.com/superphy/semantic>`__

Live: https://lfz.corefacility.ca/superphy/spfy/

Platform for predicting Serotype & Virulence Factors (via
`ECTyper <https://github.com/phac-nml/ecoli_serotyping>`__) and
Antimicrobial Resistance (via
`CARD <https://card.mcmaster.ca/analyze/rgi>`__) from E.coli genome
sequences bundled using task queues (RQ) and a SPA front-end
(AngularJS/Flask).

Use:
----

1. Install Docker (& Docker-Compose separately if you're on Linux,
   `link <https://docs.docker.com/compose/install/>`__). mac/windows
   users have Compose bundled with Docker Engine.
2. ``git clone --recursive https://github.com/superphy/backend.git``
3. ``cd backend/``
4. ``docker-compose up``
5. Visit http://localhost:8090
6. Eat cake :cake:

Architecture:
-------------

+------+------+------+------+
| Dock | Port | Name | *Des |
| er   | s    | s    | crip |
| Imag |      |      | tion |
| e    |      |      | *    |
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

Note: an earlier version of the front-end (written in AngularJS with
limited features) is still available at http://localhost:8000

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

The ``superphy/backend:2.0.0`` which runs the main web app uses
``supervisor`` to manage inner processes: ``nginx``, ``uWsgi``.

Extending:
----------

The ``blob_savvy()`` in ``/app/modules/spfy.py`` handles the separation
of multiple-file inputs into single file calls. The
``blob_savvy_enqueue()``, called by ``blob_savvy()``, manages the RQ
pipeline for processing an individual file. Say you wanted to add a
example analysis called ``penguin``: 1. NOTE: everything (rq workers,
uwsgi, etc.) run inside ``/app``, import should be relative to this.
Example:
``from modules.blazeUploader.reserve_id import write_reserve_id``. The
top-most directory is used to build Docker Images and copies the
contents of ``/app`` to run inside the containers. 2. Write a
``blob_penguin_enqueue()`` to handle your enqueueing of your
analysis-specific pipeline. 3. Add the ``blob_penguin_enqueue()`` call
to ``blob_savvy()``. 4. If you want to store the results to Blazegraph,
you can add that to your pipeline. In ``savvy``, the graph generation is
handled in ``/app/modules/turtleGrapher/datastruct_savvy.py``, you can
use that as an example. Note that the ``upload_graph()`` call is made
within ``datastruct_savvy.py``; this is done to avoid having to pass the
resulting ``rdflib.Graph`` object between tasks. Also, the base graph
(only containing information about the file, without any results from
analyses) is handled by
``/app/modules/turtleGrapher/turtle_grapher.py``. 5. If you want to
return the results to the front-end, your ``blob_penguin_enqueue()``
should return a nested dictionary in the format {*JobID*: {'file':
*filename including path*, 'analysis': *type of analysis*}} where the
italicized items are filled with the actual values and 'file'/'analysis'
are string literals. Note that the 'file'/'analysis' are recommended,
but not actually used by the front-end, only the *JobIDs* are. RQ's
``.enqueue()`` returns the JobID by default. The front-end code is
located in ``/app/static`` for the *js*/*css*/*img* files and in
``/app/templates/index.html``. Once you've added your code, you can
rebuild the docker images by doing the following in the repo root: 1.
``docker-compose down`` 2. ``docker-compose build --no-cache`` 3.
``docker-compose up``

ReCaptcha Support:
------------------

To enable: 1. Get a pair of ReCaptcha keys from Google, specific to your
site domain. 2. Uncomment the ``<!-- captcha-->`` code in
``/app/templates/index.html`` 3. In ``/app/static/main.js``, add your
public key to ``$scope.model`` dictionary under the key ``key`` 4. In
``/app/config.py`` set ``RECAPTCHA_ENABLED`` to ``True`` and add your
corresponding public and private ('site' and 'secret') keys. 5. Rebuild
your docker images.

Debugging:
----------

-  Ideally, setup a https://sentry.io account and copy your DSN into
   ``/app/config.py``
-  Alternatively:
-  Port 9181 is mapped to host on Service ``backend-rq``, you can use
   ``rq-dashboard`` via:

1. ``docker exec -it backend_worker_1 sh`` this drops a shell into the
   rq worker container which has rq-dashboard installed via conda
2. ``rq-dashboard -H redis`` runs rq-dashboard and specifies the *redis*
   host automatically defined by docker-compose
3. then on your host machine visit http://localhost:9181

Blazegraph:
-----------

-  We are currently running Blazegraph version 2.1.4. If you want to run
   Blazegraph separately, please use the same version otherwise there
   may be problems in endpoint urls / returns (namely version 2.1.1).
   See `#63 <https://github.com/superphy/backend/issues/63>`__
   Alternatively, modify the endpoint accordingly under
   ``database['blazegraph_url']`` in ``/app/config.py``

CLI-Only:
---------

-  If you wish to only create rdf graphs (serialized as turtle files):

1. First install miniconda and activate the environment from
   https://raw.githubusercontent.com/superphy/docker-flask-conda/master/app/environment.yml
2. cd into the app folder (where RQ workers typically run from):
   ``cd app/``
3. Run savvy.py like so:
   ``python -m modules/savvy -i tests/ecoli/GCA_001894495.1_ASM189449v1_genomic.fna``
   where the argument after the ``-i`` is your genome (FASTA) file.

# Ontology The ontology for Spfy is available at:
https://raw.githubusercontent.com/superphy/backend/master/app/scripts/spfy\_ontology.ttl
It was generated using
https://raw.githubusercontent.com/superphy/backend/master/app/scripts/generate\_ontology.py
with shared functions from Spfy's backend code. If you wish to run it,
do: 1. ``cd app/`` 2. ``python -m scripts/generate_ontology`` which will
put the ontology in ``app/``

.. |Build Status| image:: https://travis-ci.org/superphy/backend.svg?branch=master
   :target: https://travis-ci.org/superphy/backend
.. |GitHub license| image:: https://img.shields.io/badge/license-Apache%202-blue.svg
   :target: https://raw.githubusercontent.com/superphy/backend/master/LICENSE
