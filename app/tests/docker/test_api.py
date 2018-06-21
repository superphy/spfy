import requests
import mock
import subprocess
import config

from middleware.blazegraph.reserve_id import _check
from middleware.graphers.turtle_utils import generate_hash, generate_uri as gu

from tests.utils import listdir_fullpath

WEBSERVER_PORT = '8000'
API_ROOT = 'api/v0/'
GROUCH_PORT = '8090'

WEBSERVER = 'spfy_webserver_1'
blazegraph_url = config.database['blazegraph_url']

GENOMES_LIST_ECOLI = listdir_fullpath('tests/ecoli')

def test_api():
    '''
    This is an external test that checks if 'webserver' Flask api started correctly.
    '''
    r = requests.get("""http://localhost:{port}/{api_root}alive""".format(port=WEBSERVER_PORT,api_root=API_ROOT))
    # There is a route defined in the Flask API that returns the string 'true' when queried.
    assert r.text == 'true'



exc = """docker exec -i {webserver} sh -c""".format(webserver=WEBSERVER)

def test_api_internal():
    # Check that the subprocess setup works before running other tests.
    o = subprocess.check_output("""{exc} {cmd}""".format(exc=exc,cmd='"echo a"'), shell=True, stderr=subprocess.STDOUT)
    o = o.replace('\n', '')
    assert o == 'a'

# def test_api_internal_blazegraph():
#     # Check that 'webserver' can connect to the 'blazegraph' database.
#     cmd = '"curl {blazegraph}"'.format(blazegraph=blazegraph_url)
#     o = subprocess.check_output("""{exc} {cmd}""".format(exc=exc,cmd=cmd), shell=True, stderr=subprocess.STDOUT)
#     try:
#         assert '</rdf:RDF>' in o
#     except:
#         raise Exception('test_api_internal_blazegraph() failed with curl output: {0}'.format(o))

def test_simple_auth():
    # Retrieve a bearer token from the api.
    r = requests.get("""http://localhost:{port}/{api_root}accounts""".format(port=WEBSERVER_PORT,api_root=API_ROOT))
    token = r.text
    assert isinstance(token, (str, unicode))

    # Check the bearer token allows access to a protected ping.
    headers = {
        'Authorization': 'Bearer ' + token
    }
    r = requests.get("""http://localhost:{port}/{api_root}secured/simple/ping""".format(port=WEBSERVER_PORT,api_root=API_ROOT), headers=headers)
    assert r.text == "All good. You only get this message if you're authenticated"

def test_search(f='gi|1370526529|gb|CP027599.1|'):
    '''Checks the search api returns some jobid.
    '''
    d = {'st':f}
    r = requests.post(
        """http://localhost:{port}/{api_root}search""".format(
            port=WEBSERVER_PORT,
            api_root=API_ROOT),
        data=d)
    jobid = r.text
    assert len(jobid) == 36

def test_grouch():
    '''Checks that Grouch (the React app) is running on the expected port.
    '''
    e = '<title>Spfy: Grouch</title>'
    r = requests.get('http://localhost:{}/'.format(GROUCH_PORT))
    assert e in r.text

class MockMongo():
    def __init__(self):
        self.d = {
            'spfyid':0
        }
    def mongo_find(self, uid, key='store', collection=''):
        return self.d[uid]

    def mongo_update(self, uid, json, key='store', collection=''):
        self.d.update({uid: json})

class TestDuplicateDefaults(object):
    
    m = MockMongo()

    @mock.patch('mongo_find', side_effect=m.mongo_find)
    def test_duplicate_defaults(self):
        '''Should start spfyids at 0 and inrement by 1.
        '''
        # Disable Blazegraph lookup
        config.DATABASE_EXISTING = False
        # Disable force Mongo Spfyid at specific value.
        config.DATABASE_BYPASS = False

        # Files and URIs for testing.
        g1 = GENOMES_LIST_ECOLI[0]
        g2 = GENOMES_LIST_ECOLI[1]
        hash1 = generate_hash(g1)
        hash2 = generate_hash(g2)
        uri1 = gu(':' + hash1)
        uri2 = gu(':' + hash2)

        r1, dup1 = _check(uri1)
        assert r1 == 0
        assert not dup1

        r2, dup2 = _check(uri2)
        assert r2 == 1
        assert r1 != r2
        assert not dup2

        r3, dup3 = _check(uri1)
        assert r3 == r1
        assert dup3