import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
# Attendance Biometric
class AttendanceBiometric(Document):
    def after_insert(self):
        settings = frappe.get_single("Biometric Settings")

        if settings.employee_checkin:
            frappe.get_doc({
                "doctype": "Employee Checkin",
                "employee": self.employeeid, 
                "time": now_datetime(),
                "log_type": "IN",
                "attendance_biometric": self.name
            }).insert(ignore_permissions=True)

        if settings.attendance:
            frappe.get_doc({
                "doctype": "Attendance",
                "employee": self.employeeid,
                "attendance_date": now_datetime().date(),
                "status": "Present",  
                "attendance_biometric": self.name
            }).insert(ignore_permissions=True)

        if settings.attendance_request:
            frappe.get_doc({
                "doctype": "Attendance Request",
                "employee": self.employeeid,
                "from_date": now_datetime().date(),
                "to_date": now_datetime().date(),
                "reason": "Auto-created by Attendance Biometric",
                "status": "Open",
                "attendance_biometric": self.name
            }).insert(ignore_permissions=True)
