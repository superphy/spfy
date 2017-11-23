import requests

WEBSERVER_PORT = '8090'
API_ROOT = 'api/v0/'

def test_api():
    r = requests.get("""http://localhost:{port}/{api_root}alive""".format(port=WEBSERVER_PORT,api_root=API_ROOT))
    assert r.text == 'true'
