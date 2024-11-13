from pprint import pprint as pp
import time

from Authentication.authentication import vmanage_authenticate
from Authentication.credentials import (
    VMANAGE_BASE_URL,
    VMANAGE_API_URL
)
from Documentation.file_path import ROUTER_SIGNED_PATH
from SDWAN.sdwan_url import (
    DEVICE_LIST_URI,
    CONTROLLER_CSR_GENERATE_URI,
    EDGE_CSR_GENERATE_URI,
    TASK_STATUS_URI
)
from SDWAN.sdwan_device import SDWAN_Device


class vManage_Session:
    def __init__(self):
        self.session = vmanage_authenticate()

    def get_session(self):
        return self.session

    def get_device_list(self):
        """
        Retrieve and return network devices list. Returns information about each device that is part of the fabric.
        :param: None
        :return: (list[]) list containing SDWAN devices represented as dict() objects
        """
        url = VMANAGE_BASE_URL + VMANAGE_API_URL + DEVICE_LIST_URI
        response = self.session.get(url=url, verify=False)
        sdwan_device_list = []

        if response.ok:
            sdwan_device_list = response.json()['data']
        else:
            print(response.status_code)
            print("Failed to get list of devices " + str(response.text))
            exit()

        return sdwan_device_list

    # generate list of SDWAN device objects
    def generate_sdwan_device_list(self):
        sdwan_device_list = []

        device_dict_list = self.get_device_list()
        for device_dict in device_dict_list:
            if device_dict['validity'] == 'valid':
                device_object = SDWAN_Device(device_dict=device_dict)
                sdwan_device_list.append(device_object)

        return sdwan_device_list

    def generate_controller_csr(self, device):
        url = VMANAGE_BASE_URL + VMANAGE_API_URL + CONTROLLER_CSR_GENERATE_URI
        data = {
            "deviceIP": f"{device.get_system_ip()}"
        }
        response = self.session.post(url=url, json=data, verify=False)

        if not (response.ok and response.json()['data'][0]['state'] == 'CSR Generated'):
            print(response.status_code)
            print(f"Failed to generate CSR on controller device: {device.get_system_ip()}. " + str(response.text))
            exit()
        else:
            return response.json()['data'][0]['deviceCSR']

    def generate_edge_csr(self, device):
        url = VMANAGE_BASE_URL + VMANAGE_API_URL + EDGE_CSR_GENERATE_URI
        data = {
            "deviceUUID": f"{device.get_id()}"
        }
        response = self.session.post(url=url, json=data, verify=False)

        if not response.ok:
            if response.json()['error']['code'] == 'DEVLIFECYCLE0005':
                print("Failed to generate CSR on edge device: " + response.json()['error']['details'])
                return False
            else:
                print(response.status_code)
                print(f"Failed to generate CSR on edge device: {device.get_id()}. " + str(response.text))
                exit()
        else:
            task_id = response.json()['id']
            iterations = 0
            while not self.get_device_csr_gen_task_status(task_id):
                time.sleep(5)
                iterations += 1
                if iterations == 12:
                    print(f"cEdge router {device.get_id()} could not generate CSR within 1 minute. " + str(response.text))
                    exit()

        device_csr = self.get_cedge_certificate_details(device)
        return device_csr

    def get_device_csr_gen_task_status(self, task_id):
        url = VMANAGE_BASE_URL + VMANAGE_API_URL + TASK_STATUS_URI.format(task_id=task_id)
        response = self.session.get(url=url, verify=False)

        if not (response.ok and response.json()['data'][0]['actionType'] == 'generate_csr'):
            print(response.status_code)
            print(f"Failed to either generate task status or the 'generate_csr' task_id is incorrect. " + str(response.text))
            exit()
        else:
            return True if response.json()['data'][0]['status'] == "Success" else False

    def get_device_cert_install_task_status(self, task_id):
        url = VMANAGE_BASE_URL + VMANAGE_API_URL + TASK_STATUS_URI.format(task_id=task_id)
        response = self.session.get(url=url, verify=False)

        if not (response.ok and response.json()['data'][0]['action'] == 'install_certificate'):
            print(response.status_code)
            print(f"Failed to either generate task status or the 'install_cerificate' task_id is incorrect. " + str(response.text))
            exit()
        else:
            return True if response.json()['data'][0]['status'] == "Success" else False

    def get_cedge_certificate_details(self, device):
        url = VMANAGE_BASE_URL + VMANAGE_API_URL + "/certificate/vedge/list"
        response = self.session.get(url=url, verify=False)

        if not response.ok:
            print(response.status_code)
            print(f"Failed to get certificate details on edge device: {device.get_id()}. " + str(response.text))
            exit()
        else:
            device_csr = [device_json['vedgeCSR'] for device_json in response.json()['data']
                          if device_json['uuid'] == device.get_id()][0]
            return device_csr

    def install_cedge_signed_certificate(self, device):
        signed_cert = device.get_signed_cert()
        url = VMANAGE_BASE_URL + VMANAGE_API_URL + "/certificate/install/signedCert"
        payload = signed_cert
        response = self.session.post(url=url, data=payload, verify=False)

        if not response.ok:
            print(f"Failed to install certificate of edge device: {device.get_id()}. " + str(response.text))
            exit()
        else:
            task_id = response.json()['id']
            iterations = 0
            while not self.get_device_cert_install_task_status(task_id):
                time.sleep(5)
                iterations += 1
                if iterations == 24:
                    print(f"cEdge router {device.get_id()} could not install certificate within 2 minutes. " + str(response.text))
                    exit()


if __name__ == '__main__':
    session = vManage_Session()
    pp(session.get_device_list())
    # session.install_cedge_signed_certificate(device=None)
    # generate_controller_csr(controller_system_ip="10.10.10.2")  # vBond

    # C8200-R1: C8200-1N-4T-FJC26321D8E, C8200-R2: C8200-1N-4T-FJC26321D99, IR1835: IR1835-K9-FCW2541Z064
    # pp(generate_edge_csr(device=C8200_R1_object))  # C8200-R1
    # pp(generate_edge_csr(device=C8200_R2_object))  # C8200-R2
    # pp(generate_edge_csr(device=IR1835_object))  # IR1835
    # pp(get_cedge_certificate_details(C8200_R1_object))
    # pp(get_device_task_status(task_id="d675bc90-d546-4236-98ee-175ba6afb0e2"))
