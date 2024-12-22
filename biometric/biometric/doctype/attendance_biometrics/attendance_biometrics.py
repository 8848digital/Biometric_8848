import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from datetime import datetime

class AttendanceBiometrics(Document):
    def after_insert(self):
        try:
            settings = frappe.get_single("Biometric Settings")
            if not hasattr(self, 'devicecode'):
                frappe.throw(_("Device code is missing from Attendance Biometric document"))
            if not self.logdatetime:
                raise ValueError("logdatetime is missing or empty in Attendance Biometric document.")
            
            employee_ids = frappe.get_all("Employee", filters={"attendance_device_id": self.devicecode}, fields=["name", "attendance_device_id"])

            for employee in employee_ids:
                try:
                    logdatetime = datetime.strptime(self.logdatetime, "%Y-%m-%d %H:%M:%S")
                except ValueError as e:
                    frappe.get_doc({
                        "doctype": "Biometric Error Log",
                        "title": "Error in AttendanceBiometric after_insert",
                        "time_stamp": now_datetime(),
                        "details": f"Error parsing logdatetime: {str(e)} - logdatetime value: '{self.logdatetime}'"
                    }).insert(ignore_permissions=True)
                    frappe.log_error(f"Error parsing logdatetime: {str(e)} - logdatetime value: '{self.logdatetime}'", "AttendanceBiometric Error")
                    raise

                log_type = "IN" if logdatetime.hour < 12 else "OUT"

                if settings.employee_checkin:
                    frappe.get_doc({
                        "doctype": "Employee Checkin",
                        "employee": employee['name'],
                        "time": self.logdatetime,
                        "log_type": log_type,
                        "attendance_biometric": self.name
                    }).insert(ignore_permissions=True)

                if settings.attendance:
                    frappe.get_doc({
                        "doctype": "Attendance",
                        "employee": employee['name'],
                        "attendance_date": self.logdatetime,
                        "status": "Present",  
                        "attendance_biometric": self.name
                    }).insert(ignore_permissions=True)

                if settings.attendance_request:
                    frappe.get_doc({
                        "doctype": "Attendance Request",
                        "employee": employee['name'],
                        "from_date": self.logdatetime,
                        "to_date": self.logdatetime,
                        "reason": "ON Duty",
                        "status": "Open",
                        "attendance_biometric": self.name
                    }).insert(ignore_permissions=True)

            # Log Success Message for after_insert operation
            frappe.get_doc({
                "doctype": "Attendance Biometric Error Log",
                "title": "Success in AttendanceBiometric after_insert",
                "time_stamp": now_datetime(),
                "details": f"AttendanceBiometric document {self.name} processed successfully."
            }).insert(ignore_permissions=True)
        
        except Exception as e:
            # Log Error Message in case of failure
            frappe.get_doc({
                "doctype": "Attendance Biometric Error Log",
                "title": "Error in AttendanceBiometric after_insert",
                "time_stamp": now_datetime(),
                "details": str(e)
            }).insert(ignore_permissions=True)
            frappe.db.rollback()
            frappe.db.commit()
            frappe.log_error(f"Error in AttendanceBiometric after_insert: {str(e)}", "AttendanceBiometric Error")
            raise
