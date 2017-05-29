#for secret key, do a os.urandom(24).encode('hex')
SECRET_KEY = 'is-that-daisy'
REDIS_URL = 'redis://redis:6379/0'
# actual queues aren't defined here, they are in their respective supervisord.conf worker call
# this is done to isolate the RQ-Blazegraph worker to avoid race conditions
QUEUES = ['default']
# QUEUES_SPFY is for spfy web-app to poll
QUEUES_SPFY = ['singles', 'blazegraph', 'multiples']
BOOTSTRAP_SERVE_LOCAL = True
MAX_TIME_TO_WAIT = 10

DATASTORE = '/datastore'
RECAPTCHA_ENABLED = False
RECAPTCHA_SITE_KEY = "6LeVYhgUAAAAAKbedEJoCcRaeFaxPh-2hZfzXfFP"
RECAPTCHA_SECRET_KEY = "PUTYOSECRETKEYHERE"

#### this is from savvy.py

#rdf namespaces
namespaces = {
    'root' : 'https://www.github.com/superphy#',
    'ge' : 'http://purl.obolibrary.org/obo/GENEPIO_',
    'g' : 'http://www.biointerchange.org/gfvo#',
    'obi' : 'http://purl.obolibrary.org/obo/OBI_',
    'envo' : 'http://purl.obolibrary.org/obo/ENVO_',
    'doid' : 'http://purl.obolibrary.org/obo/DOID_',
    'faldo' : 'http://biohackathon.org/resource/faldo#',
    'ncbi' : 'http://purl.obolibrary.org/obo/NCBI_Taxon_',
    'so' : 'http://purl.obolibrary.org/obo/SO_',
    'dc' : 'http://purl.org/dc/elements/1.1/',
    'rdf' : 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'owl' : 'http://www.w3.org/2002/07/owl#',
    'rdfs' : 'http://www.w3.org/2000/01/rdf-schema#'
}

#database defaults
DATABASE_ENABLED = True
database = {}
database['blazegraph_url'] = 'http://blazegraph:8080/bigdata/sparql'
#database['blazegraph_url'] = 'http://localhost:9000/blazegraph/namespace/superphy/sparql'
#### end of savvy.py stuff


# Sentry DSN for RQ; note: RQ also reads from REDIS_URL, and QUEUES
# If you're using Sentry to collect your runtime exceptions, you can use this
# to configure RQ for it in a single step
# NOTE!!!: There is a bug with Raven that needs to be accounted for in RQ config. You must prefix your sentry dsn with sync+ eg 'sync+https://...' see https://github.com/nvie/rq/issues/350 . As of Mar.'17 this hasn't been fixed.
#SENTRY_DSN = 'sync+https://public:secret@example.com/1'
