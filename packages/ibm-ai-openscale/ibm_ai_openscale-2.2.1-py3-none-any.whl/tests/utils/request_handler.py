import requests
from requests.adapters import HTTPAdapter
from .configuration import get_aios_credentials, is_icp

host = get_aios_credentials()['url']

aios_adapter = HTTPAdapter(max_retries=3)
request_session = requests.Session()
request_session.mount(host, aios_adapter)

if is_icp():
    request_session.verify = False
