import os

#for secret key, do a os.urandom(24).encode('hex')
SECRET_KEY = 'is-that-daisy'
REDIS_URL = 'redis://redis:6379/0'
QUEUES = ['high','medium','low','default']
BOOTSTRAP_SERVE_LOCAL = True
MAX_TIME_TO_WAIT = 10

UPLOAD_FOLDER = 'app/tmp'
ALLOWED_EXTENSIONS = ['fna']
RECAPTCHA_ENABLED = True
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
    'rdf' : 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
}

#database defaults
database = {}
database['blazegraph_url'] = 'http://localhost:9000/blazegraph/namespace/superphy/sparql'
#database['blazegraph_url'] = 'http://localhost:9000/blazegraph/namespace/superphy/sparql'
#note: the convention here is database['count'] is NOT occupied
# on new DB, start at 1
database['count'] = 1
#### end of savvy.py stuff


# Sentry DSN for RQ; note: RQ also reads from REDIS_URL, and QUEUES
# If you're using Sentry to collect your runtime exceptions, you can use this
# to configure RQ for it in a single step
#SENTRY_DSN = 'http://public:secret@example.com/1'
