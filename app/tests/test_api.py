import requests

WEBSERVER_PORT = '8090'
API_ROOT = 'api/v0/'

def test_api():
    '''
    This is an external test that checks if 'webserver' Flask api build correctly.
    '''
    r = requests.get("""http://localhost:{port}/{api_root}alive""".format(port=WEBSERVER_PORT,api_root=API_ROOT))
    # There is a route defined in the Flask API that returns the string 'true' when queried.
    assert r.text == 'true'

import subprocess
import config

WEBSERVER = 'backend_webserver_1'
blazegraph_url = config.database['blazegraph_url']

def test_api_internal():
    # Check that the subprocess setup works before running other tests.
    exc = """docker exec -i {webserver} sh -c""".format(webserver=WEBSERVER)
    o = subprocess.check_output("""{exc} {cmd}""".format(exc=exc,cmd='"echo a"'), shell=True, stderr=subprocess.STDOUT)
    o = o.replace('\n', '')
    assert o == 'a'

    # Check that 'webserver' can connect to 'blazegraph'
    cmd = "curl {blazegraph}".format(blazegraph=blazegraph_url)
    o = subprocess.check_output("""{exc} {cmd}""".format(exc=exc,cmd=cmd), shell=True, stderr=subprocess.STDOUT)
    assert 'Welcome to Blazegraph Database!' in o
