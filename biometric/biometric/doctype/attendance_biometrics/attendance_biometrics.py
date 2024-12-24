import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from datetime import datetime

class AttendanceBiometrics(Document):
    def after_insert(self):
        try:
            # Fetch Biometric Settings
            settings = frappe.get_single("Biometric Settings")
            
            # Validate devicecode field
            if not hasattr(self, 'devicecode') or not self.devicecode:
                frappe.throw(_("Employee ID is missing from Attendance Biometric document"))
            
            # Fetch employees matching the device code
            employee_ids = frappe.get_all(
                "Employee", 
                filters={"attendance_device_id": self.devicecode}, 
                fields=["name", "attendance_device_id"]
            )
            
            # Validate logdatetime format
            try:
                logdatetime = datetime.strptime(self.logdatetime, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                frappe.throw(_("Invalid logdatetime format. Expected '%Y-%m-%d %H:%M:%S'"))
            
            log_type = "IN" if logdatetime.hour < 12 else "OUT"
            
            # Process settings and create relevant documents
            for employee in employee_ids:
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
                        "reason": "On Duty",
                        "status": "Open",
                        "attendance_biometric": self.name
                    }).insert(ignore_permissions=True)
            
            # Log success if enabled in settings
            if settings.attendance_biometric_error_log:
                frappe.get_doc({
                    "doctype": "Attendance Biometric Error Log",
                    "title": "Success in AttendanceBiometric",
                    "time_stamp": now_datetime(),
                    "details": "AttendanceBiometric processed successfully"
                }).insert(ignore_permissions=True)

        except Exception as e:
            # Log error if enabled in settings
            if settings and settings.attendance_biometric_error_log:
                frappe.get_doc({
                    "doctype": "Attendance Biometric Error Log",
                    "title": "Error in AttendanceBiometric",
                    "time_stamp": now_datetime(),
                    "details": str(e)
                }).insert(ignore_permissions=True)
        
        finally:
            # Commit changes to the database
            frappe.db.commit()
