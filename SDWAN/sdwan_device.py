from pprint import pformat


class SDWAN_Device:
    def __init__(self, device_dict):
        # instantiate SD-WAN device object solely with necessary fields.
        self.id = device_dict['uuid']
        self.model = device_dict['deviceModel']
        self.type = device_dict['deviceType']
        self.hostname = device_dict['host-name'] if 'host-name' in device_dict else device_dict['uuid']
        self.system_ip = device_dict['system-ip']
        self.platform = device_dict['platformFamily']
        self.connected_vmanage = device_dict['vmanage-system-ip']
        self.site_id = device_dict['site-id']
        self.site_name = device_dict['site-name']
        self.validity = device_dict['validity']
        self.csr = device_dict['deviceCSR'] if 'deviceCSR' in device_dict else None
        self.csr_id = None
        self.signed_cert = device_dict['deviceEnterpriseCertificate'] if 'deviceEnterpriseCertificate' in device_dict else None
        self.expiration = device_dict['expirationDate'] if device_dict['expirationDate'] != 'NA' else None
        self.version = device_dict['version']

    def get_id(self):
        return self.id

    def get_hostname(self):
        return self.hostname

    def get_type(self):
        return self.type

    def get_csr(self):
        return self.csr.strip() if self.csr is not None else ""

    def get_csr_id(self):
        return self.csr_id if self.csr_id is not None else ""

    def get_signed_cert(self):
        return self.signed_cert.strip() if self.signed_cert is not None else ""

    def get_system_ip(self):
        return self.system_ip

    def get_device_model(self):
        return self.model

    def set_csr(self, csr):
        self.csr = csr

    def set_csr_id(self, csr_id):
        self.csr_id = csr_id

    def set_signed_cert(self, signed_cert):
        self.signed_cert = signed_cert

    def __str__(self):
        return pformat({
            "id": str(self.id),
            "type": str(self.type),
            "hostname": str(self.hostname),
            "model": str(self.model),
            "system_ip": str(self.system_ip),
            "site_id": str(self.site_id),
            "version": str(self.version),
            "validity": str(self.validity),
            "expiration": str(self.expiration)
        })
