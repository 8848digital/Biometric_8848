import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from datetime import datetime

class AttendanceBiometric(Document):
    def after_insert(self):
        settings = frappe.get_single("Biometric Settings")
        
        if not hasattr(self, 'employeeid'):
            frappe.throw(_("Employee ID is missing from Attendance Biometric document"))
        
        employee_ids = frappe.get_all("Employee", filters={"attendance_device_id": self.employeeid}, fields=["name", "attendance_device_id"])

        for employee in employee_ids:
            intime = datetime.strptime(self.intime, "%Y-%m-%d %H:%M:%S")
            log_type = "IN" if intime.hour < 12 else "OUT"

            if settings.employee_checkin:
                frappe.get_doc({
                    "doctype": "Employee Checkin",
                    "employee": employee['name'],
                    "time": self.intime,
                    "log_type": log_type,
                    "attendance_biometric": self.name
                }).insert(ignore_permissions=True)

            if settings.attendance:
                frappe.get_doc({
                    "doctype": "Attendance",
                    "employee": employee['name'],
                    "attendance_date": self.intime,
                    "status": "Present",  
                    "attendance_biometric": self.name
                }).insert(ignore_permissions=True)

            if settings.attendance_request:
                frappe.get_doc({
                    "doctype": "Attendance Request",
                    "employee": employee['name'],
                    "from_date": self.intime,
                    "to_date": self.outtime,
                    "reason": "Auto-created by Attendance Biometric",
                    "status": "Open",
                    "attendance_biometric": self.name
                }).insert(ignore_permissions=True)
