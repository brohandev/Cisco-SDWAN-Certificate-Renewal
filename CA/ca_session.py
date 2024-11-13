from bs4 import BeautifulSoup
from pprint import pprint as pp

from Authentication.authentication import (
    ca_authenticate
)
from Authentication.credentials import (
    CERTIFICATE_AUTHORITY_URL
)
from CA.ca_url import (
    CA_SEND_CSR_URI
)


class CA_Session:
    def __init__(self):
        self.session = ca_authenticate()

    def get_session(self):
        return self.session

    def send_device_csr_to_ca(self, device):
        csr = device.get_csr()
        url = CERTIFICATE_AUTHORITY_URL + CA_SEND_CSR_URI
        payload = {
            'Mode': 'newreq',
            'SaveCert': 'yes',
            'CertRequest': f'{csr.strip()}'
        }
        response = self.session.post(url=url, data=payload, verify=False)

        try:
            if response.ok:
                response_html = response.content.decode('utf-8')
                soup = BeautifulSoup(response_html, 'html.parser')
                # req_msg = soup.find(id="locInfoNewReq").text
                req_id_content = soup.find(id="locInfoReqID").text
                req_id = [int(i) for i in req_id_content.split(".")[0].split() if i.isdigit()][0]

                return req_id
            else:
                print(response.status_code)
                print("Failed to get list of devices " + str(response.content))
                exit()
        except Exception as error:
            print("Exception while parsing HTML response occurred:", error)

    def retrieve_device_signed_cert_from_ca(self, device):
        csr_id = device.get_csr_id()
        url = CERTIFICATE_AUTHORITY_URL + f"/certsrv/certnew.cer?ReqID={csr_id}&Enc=b64.asp"
        response = self.session.get(url=url, verify=False)

        try:
            if response.ok:
                return response.text.strip()
            else:
                print(response.status_code)
                print("Failed to retrieve signed certificate content from CA " + str(response.text))
                exit()
        except Exception as error:
            print("Exception while retrieving signed certificate from CA occurred:", error)


if __name__ == '__main__':
    # csr = open(EXAMPLE_CSR_PATH, "r").read()
    # C8200_R1_object.set_csr(
    #     csr=csr
    # )
    # pp(C8200_R1_object.get_csr())
    session = CA_Session()
    # session.send_device_csr_to_ca(device=C8200_R1_object)
    # session.retrieve_device_signed_cert_from_ca()
