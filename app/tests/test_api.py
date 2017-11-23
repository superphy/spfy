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
    exc = 'docker exec -ti {webserver} sh -c'.format(webserver=WEBSERVER)
    o = subprocess.check_output(' "{cmd}"'.format(cmd='echo a'), shell=True, stderr=subprocess.STDOUT)
    assert o == 'a'
