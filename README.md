[![Build Status](https://travis-ci.org/superphy/backend.svg?branch=master)](https://travis-ci.org/superphy/backend)
[![GitHub license](https://img.shields.io/badge/license-Apache%202-blue.svg)](https://raw.githubusercontent.com/superphy/backend/master/LICENSE)

**Spfy**: speedy [superphy](https://github.com/superphy/semantic)

Live: https://lfz.corefacility.ca/superphy/spfy/

Platform for predicting Serotype & Virulence Factors (via [ECTyper](https://github.com/phac-nml/ecoli_serotyping)) and Antimicrobial Resistance (via [CARD](https://card.mcmaster.ca/analyze/rgi)) from E.coli genome sequences bundled using task queues (RQ) and a SPA front-end (AngularJS/Flask).

## Use:
1. Install Docker (& Docker-Compose separately if you're on Linux, [link](https://docs.docker.com/compose/install/)). mac/windows users have Compose bundled with Docker Engine.
2. `git clone https://github.com/superphy/backend.git`
3. `cd backend/`
4. `git submodule update --init --remote --recursive`
5. `docker-compose up`
6. Visit http://localhost:8000
7. Eat cake :cake:

## Architecture:
Docker Image | Ports | Names | *Description*
--- | --- | --- | ---
superphy/backend-rq:2.0.0 | 80/tcp, 443/tcp | backend_worker_1 | the main redis queue workers
superphy/backend-rq-blazegraph:2.0.0 | 80/tcp, 443/tcp | backend_worker-blazegraph-ids_1 | this handles spfyID generation for the blazegraph database
superphy/backend:2.0.0 | 0.0.0.0:80->80/tcp, 443/tcp | backend_web-nginx-uwsgi_1 | the actual web app interface
superphy/blazegraph:2.1.4 | 0.0.0.0:8080->8080/tcp | backend_blazegraph_1 | Blazegraph Database
redis:3.2 | 6379/tcp | backend_redis_1 | Redis Database

## Further Details:
The `superphy/backend-rq:2.0.0` image is *scalable*: you can create as many instances as you need/have processing power for. The image is responsible for listening to the `multiples` queue (12 workers) which handles most of the tasks, including `RGI` calls. It also listens to the `singles` queue (1 worker) which runs `ECTyper`. This is done as `RGI` is the slowest part of the equation. Worker management in handled in `supervisor`.

The `superphy/backend-rq-blazegraph:2.0.0` image is not scalable: it is responsible for querying the Blazegraph database for duplicate entries and for assigning spfyIDs in *sequential* order. It's functions are kept as minimal as possible to improve performance (as ID generation is the one bottleneck in otherwise parallel pipelines); comparisons are done by sha1 hashes of the submitted files and non-duplicates have their IDs reserved by linking the generated spfyID to the file hash. Worker management in handled in `supervisor`.

The `superphy/backend:2.0.0` which runs the main web app uses `supervisor` to manage inner processes: `nginx`, `uWsgi`.

## Extending:
