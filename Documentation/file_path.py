import os


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
ROUTER_CSR_PATH = BASE_DIR + "/cert_signing_requests/router"
CONTROLLER_CSR_PATH = BASE_DIR + "/cert_signing_requests/controller"
ROUTER_SIGNED_PATH = BASE_DIR + "/cert_signed/router"
CONTROLLER_SIGNED_PATH = BASE_DIR + "/cert_signed/controller"
