from pprint import pprint as pp

from Auxiliary.auxiliary import store_device_csr, store_device_signed_cert
from CA.ca_session import CA_Session
from SDWAN.vmanage_session import vManage_Session
from SDWAN.sdwan_device import SDWAN_Device


class Certificate_Renewal_Process:
    def __init__(self):
        self.ca_session = CA_Session()
        self.vmanage_session = vManage_Session()
        self.router_list = list()
        self.controller_list = list()
        self.failed_router_list = list()
        self.failed_controller_list = list()
        self.csr_id_list = list()

    def initialize_device_list(self):
        # Step 1: Retrieve list of all SDWAN devices, store routers and controllers in persistent class lists
        device_list = self.vmanage_session.generate_sdwan_device_list()
        for device in device_list:
            if SDWAN_Device.get_type(device) in ['vmanage', 'vsmart', 'vbond']:
                self.controller_list.append(device)
            else:
                if SDWAN_Device.get_device_model(device) != 'vedge-C8000V':
                    self.router_list.append(device)
        pp(self.router_list)

    def generate_csr(self):
        # # Step 2a: Generate CSR on all SDWAN controllers and store CSRs
        # for device in self.controller_list:
        #     csr = self.vmanage_session.generate_controller_csr(device=device)
        #     device.set_csr(csr=csr)
        #     store_device_csr(device)

        # print("CSRs for controllers generated")

        # Step 2b: Generate CSR on all SDWAN cEdge routers and store CSRs
        for device in self.router_list[:]:
            csr = self.vmanage_session.generate_edge_csr(device=device)
            if not csr:
                self.failed_router_list.append(device)
                self.router_list.remove(device)
            else:
                device.set_csr(csr=csr)
                store_device_csr(device)

        print("CSRs for routers generated")

    def send_csr_to_ca(self):
        # # Step 3a: Send SDWAN controllers' CSRs to CA, the CSRs will be stored inside 'Pending' folder
        # for device in self.controller_list:
        #     csr_id = self.ca_session.send_device_csr_to_ca(device=device)
        #     device.set_csr_id(csr_id=csr_id)
        #     self.csr_id_list.append({
        #         csr_id: device
        #     })

        # print("Generated CSRs for controllers sent to CA")

        # Step 3b: Send SDWAN routers' CSRs to CA, the CSRs will be stored inside 'Pending' folder
        for device in self.router_list:
            csr_id = self.ca_session.send_device_csr_to_ca(device=device)
            device.set_csr_id(csr_id=csr_id)
            self.csr_id_list.append({
                csr_id: device
            })

        print("Generated CSRs for routers sent to CA")
        pp("CSR Task IDs: " + str(self.csr_id_list) + " are currently pending requests")

    def admin_sign_csr(self):
        # Step 4: Network Administrator must sign CSRs stored inside CA manually. Proceed after doing so.
        print("Please navigate to the 'Pending Requests' folder of the CA. Highlight all pending CSRs, right-click "
              "and navigate 'All Tasks' > 'Issue'. The CSRs should be removed from the 'Pending Requests' folder and "
              "are inside 'Issued Certificates' folder. ")
        action = input("Proceed with signed certificate retrieval? (Y/N) ")
        if action.upper() != 'Y':
            print("Network administrator failed to issue signed certificates")
            exit()

    def retrieve_signed_cert_from_ca(self):
        # # Step 5a: Retrieve controller signed certificates from CA and store inside device field
        # for device in self.controller_list:
        #     signed_cert = self.ca_session.retrieve_device_signed_cert_from_ca(device=device)
        #     device.set_signed_cert(signed_cert=signed_cert)
        #     store_device_signed_cert(device=device)
        #
        # print("Retrieved signed certificates of controllers from Certificate Authority")

        # Step 5b: Retrieve router signed certificates from CA and store inside device field
        for device in self.router_list:
            signed_cert = self.ca_session.retrieve_device_signed_cert_from_ca(device=device)
            device.set_signed_cert(signed_cert=signed_cert)
            store_device_signed_cert(device=device)

        print("Retrieved signed certificates of routers from Certificate Authority")

    def install_signed_cert_on_vmanage(self):
        # # Step 6a: Install controller signed certificates into vManage
        # for device in self.controller_list:
        #     self.vmanage_session.install_cedge_signed_certificate(device=device)
        #
        # print("Installed signed certificates of controllers in vManage")

        # Step 6b: Install router signed certificates into vManage
        for device in self.router_list:
            self.vmanage_session.install_cedge_signed_certificate(device=device)

        print("Installed signed certificates of routers in vManage")


if __name__ == '__main__':
    process = Certificate_Renewal_Process()
    process.initialize_device_list()
