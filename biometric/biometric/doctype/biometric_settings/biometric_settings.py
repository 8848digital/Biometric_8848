import frappe
from frappe.model.document import Document

class BiometricSettings(Document):
    def validate(self):
        self.validate_api_credentials()

    def validate_api_credentials(self):
        if not self.api_key or not self.api_secret:
            frappe.throw("API Key and API Secret are mandatory.")

        # Check if User with the provided API Key and Secret exists
        user = frappe.db.exists("User", {
            "api_key": self.api_key,
            "api_secret": self.api_secret
        })

        if not user:
            frappe.throw("Invalid API Key or API Secret. Please check your credentials.")
