from dotenv import dotenv_values
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
ENV_DIR = BASE_DIR + "/.env"
credentials = dotenv_values(ENV_DIR)

# [CA] Certificate Authority Credentials
CERTIFICATE_AUTHORITY_URL = credentials['CERTIFICATE_AUTHORITY_URL']

# [SD-WAN] vManage Credentials
VMANAGE_BASE_URL = credentials['VMANAGE_BASE_URL']
VMANAGE_API_URL = "/dataservice"
VMANAGE_AUTH_SESSION_URL = VMANAGE_BASE_URL + '/j_security_check'
VMANAGE_AUTH_TOKEN_URL = VMANAGE_BASE_URL + '/dataservice/client/token'
VMANAGE_USERNAME = credentials['VMANAGE_USERNAME']
VMANAGE_PASSWORD = credentials['VMANAGE_PASSWORD']


if __name__ == '__main__':
    print(credentials['VMANAGE_BASE_URL'])
    print(type(credentials['VMANAGE_USERNAME']))
    # print(ENV_DIR)
