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

WEBSERVER = 'backend_webserver_1'

def test_api_internal():
    o = subprocess.check_output('docker exec -ti {webserver} sh -c "echo a"'.format(webserver=WEBSERVER))
    assert o == 'a'
