**Spfy**: speedy [superphy](https://github.com/superphy/semantic)
Web-app bundling Serotype & Virulence Factors (via [ECTyper](https://github.com/phac-nml/ecoli_serotyping)) and Antimicrobial Resistance (via [CARD](https://card.mcmaster.ca/analyze/rgi)) predictions of E.coli genome sequences.

## Use:
1. Install Docker (& Docker-Compose separately if you're on Linux [Link](https://docs.docker.com/compose/install/), mac/windows users have Compose bundled with Docker Engine)
2. `git clone https://github.com/superphy/backend.git`
3. `docker-compose up`
4. Visit http://localhost:80
5. Eat cake :cake:


## Architecture:
Docker Image | Ports | Names | *Description*
--- | --- | --- | ---
superphy/backend-rq:2.0.0 | 80/tcp, 443/tcp | backend_worker_1 | the main redis queue workers
superphy/backend-rq-blazegraph:2.0.0 | 80/tcp, 443/tcp | backend_worker-blazegraph-ids_1 | this handles spfyID generation for the blazegraph database
superphy/backend:2.0.0 | 0.0.0.0:80->80/tcp, 443/tcp | backend_web-nginx-uwsgi_1 | the actual web app interface
superphy/blazegraph:2.1.4 | 0.0.0.0:8080->8080/tcp | backend_blazegraph_1 | Blazegraph Database
redis:3.2 | 6379/tcp | backend_redis_1 | Redis Database
