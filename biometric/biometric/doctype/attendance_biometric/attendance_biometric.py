import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class AttendanceBiometric(Document):
    def validate(self, method=None):
        # Ensure employeecode is provided
        if not self.employeecode:
            frappe.throw("Employee Code (employeecode) is required to proceed.")

        # Fetch employee based on employeecode
        employee = frappe.db.get_value("Employee", {"attendance_device_id": self.employeecode}, "name")
        if not employee:
            frappe.throw(f"No Employee found with Attendance Device ID: {self.employeecode}")

        # Check if employee_checkin is enabled in Biometric Settings
        employee_checkin_enabled = frappe.db.get_value("Biometric Settings", None, "employee_checkin")
        if employee_checkin_enabled:
            new_checkin = frappe.get_doc({
                "doctype": "Employee Checkin",
                "employee": employee,
                "log_type": "IN",
                "time": now_datetime(),
                "device_id": self.employeecode
            })
            new_checkin.insert(ignore_permissions=True)

        # Check if attendance is enabled in Biometric Settings
        attendance_enabled = frappe.db.get_value("Biometric Settings", None, "attendance")
        if attendance_enabled:
            new_attendance = frappe.get_doc({
                "doctype": "Attendance",
                "employee": employee,
                "attendance_date": frappe.utils.nowdate(),
                "status": "Present"  # Adjust this as per your requirement
            })
            new_attendance.insert(ignore_permissions=True)

        # Check if attendance_request is enabled in Biometric Settings
        attendance_request_enabled = frappe.db.get_value("Biometric Settings", None, "attendance_request")
        if attendance_request_enabled:
            new_attendance_request = frappe.get_doc({
                "doctype": "Attendance Request",
                "employee": employee,
                "attendance_date": frappe.utils.nowdate(),
                "status": "Open"  # Adjust as needed
            })
            new_attendance_request.insert(ignore_permissions=True)

        # Commit changes and notify success
        frappe.db.commit()
        frappe.msgprint(f"Employee Checkin and related records created successfully for Employee: {employee}")
