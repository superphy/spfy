import requests

WEBSERVER_PORT = '8090'
API_ROOT = 'api/v0/'

def test_api():
    r = requests.get("""http://localhost:{port}/{api_root}alive""".format(port=WEBSERVER_PORT,api_root=API_ROOT))
    # There is a route defined in the Flask API that returns the string 'true' when queried.
    assert r.text == 'true'
