from pprint import pprint as pp

from Documentation.file_path import (
    CONTROLLER_CSR_PATH,
    CONTROLLER_SIGNED_PATH,
    ROUTER_CSR_PATH,
    ROUTER_SIGNED_PATH
)


# filter list of SDWAN devices to only contain control components
def generate_sdwan_controller_list(sdwan_device_list):
    controller_models_list = ['vmanage', 'vsmart', 'vbond']
    return [device for device in sdwan_device_list if device.get_type() in controller_models_list]


# store certificate signings requests for all devices inside a folder
def store_device_csr(device):
    # retrieve csr string from sdwan_device object
    csr = device.get_csr()

    # write csr to a .crt file in cert_signing_requests directory
    device_type = device.get_type()
    device_hostname = device.get_hostname()

    csr_file = None
    if device_type == 'vedge':
        csr_file = open(ROUTER_CSR_PATH + f"/{device_type}-{device_hostname}.crt", "w")
    elif device_type in ['vmanage', 'vsmart', 'vbond']:
        csr_file = open(CONTROLLER_CSR_PATH + f"/{device_type}-{device_hostname}.crt", "w")

    csr_file.write(csr)
    csr_file.close()


def store_device_signed_cert(device):
    # retrieve signed cert string from sdwan_device object
    signed_cert = device.get_signed_cert()

    # write csr to a .crt file in cert_signing_requests directory
    device_type = device.get_type()
    device_hostname = device.get_hostname()

    signed_cert_file = None
    if device_type == 'vedge':
        signed_cert_file = open(ROUTER_SIGNED_PATH + f"/{device_type}-{device_hostname}.pem", "w")
    elif device_type in ['vmanage', 'vsmart', 'vbond']:
        signed_cert_file = open(CONTROLLER_SIGNED_PATH + f"/{device_type}-{device_hostname}.pem", "w")

    signed_cert_file.write(signed_cert)
    signed_cert_file.close()
