from SDWAN.certificate_renewal import Certificate_Renewal_Process


def orchestrate():
    process = Certificate_Renewal_Process()
    process.initialize_device_list()
    process.generate_csr()
    process.send_csr_to_ca()
    process.admin_sign_csr()
    process.retrieve_signed_cert_from_ca()
    process.install_signed_cert_on_vmanage()


if __name__ == '__main__':
    orchestrate()
