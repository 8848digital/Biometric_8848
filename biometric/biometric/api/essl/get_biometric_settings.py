import frappe

@frappe.whitelist(allow_guest=True)
def biometric_settings(**kwargs):
    biometric_settings = frappe.get_doc("Biometric Settings")
    return biometric_settings.as_dict()
