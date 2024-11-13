import logging
import warnings

from Auxiliary import logging_config
import requests
from prettyprinter import pprint as pp
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from urllib3.exceptions import InsecureRequestWarning

from Authentication.credentials import (
    VMANAGE_AUTH_SESSION_URL,
    VMANAGE_AUTH_TOKEN_URL,
    VMANAGE_USERNAME,
    VMANAGE_PASSWORD
)

log = logging.getLogger(__name__)
log.propagate = False
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def vmanage_authenticate():
    """
        Creates a Session object and authenticates with the vManage node. 2 separate GET requests are made to retrieve
        Session_ID and X-XRF Token. Upon successful retrieval, the Session object is updated with the 2 fields in the
        header and returned to the caller. Upon failure during any of the previous steps, the program stops and exits.
    """

    session = requests.Session()
    vmanage_session_id = None
    vmanage_x_xsrf_token = None

    payload = {
        "j_username": VMANAGE_USERNAME,
        "j_password": VMANAGE_PASSWORD
    }

    try:
        response = requests.post(url=VMANAGE_AUTH_SESSION_URL,
                                 data=payload,
                                 verify=False)
        if response.ok:
            cookies = response.headers["Set-Cookie"]
            vmanage_session_id = cookies.split(";")[0]
        else:
            log.error("vManage Authentication Failed: Retrieving Session ID")
            exit()

        response = requests.get(url=VMANAGE_AUTH_TOKEN_URL,
                                headers={"Cookie": vmanage_session_id},
                                verify=False)
        if response.ok:
            vmanage_x_xsrf_token = response.text
        else:
            log.error("vManage Authentication Failed: Retrieving Session Token")
            exit()
    except:
        log.error("vManage Authentication: Failed to make a POST request to vManage API. Check URL and Credentials")
        exit()

    if vmanage_x_xsrf_token is not None:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': vmanage_session_id,
            'X-XSRF-TOKEN': vmanage_x_xsrf_token
        }
    else:
        headers = {
            'Content-Type': "application/json",
            'Cookie': vmanage_session_id
        }

    session.headers.update(headers)
    log.info("vManage Authentication: Authentication Successful")
    log.info("vManage Session Established")
    return session


def ca_authenticate():
    session = requests.Session()

    headers = {
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "en-US",
        'Connection': "keep-alive"
    }
    session.headers.update(headers)
    log.info("CA Server Session Headers Updated")

    return session


if __name__ == '__main__':
    vmanage_session = vmanage_authenticate()
    ca_session = ca_authenticate()
