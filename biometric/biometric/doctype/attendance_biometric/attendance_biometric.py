import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from datetime import datetime

class AttendanceBiometric(Document):
    def after_insert(self):
        try:
            settings = frappe.get_single("Biometric Settings")
            if not self.devicecode:
                frappe.throw(_("Device code is missing from Attendance Biometric document"))
            employees = frappe.get_all(
                "Employee",
                filters={"attendance_device_id": self.devicecode},
                fields=["name"]
            )
            if not employees:
                frappe.throw(_("No employees found with the provided device code"))
            try:
                logdatetime = datetime.strptime(self.logdatetime, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                frappe.throw(_("Invalid logdatetime format. Expected '%Y-%m-%d %H:%M:%S'"))

            # Determine log type (IN or OUT)
            log_type = "IN" if logdatetime.hour < 12 else "OUT"

            for employee in employees:
                employee_name = employee["name"]

                # Check for duplicate Employee Checkin
                checkin_exists = frappe.db.exists(
                    "Employee Checkin",
                    {
                        "employee": employee_name,
                        "log_type": log_type,
                        "time": self.logdatetime
                    }
                )

                if not checkin_exists:
                    last_checkin = frappe.get_all(
                        "Employee Checkin",
                        filters={
                            "employee": employee_name,
                            "time": ["<", self.logdatetime]
                        },
                        fields=["log_type"],
                        order_by="time desc",
                        limit=1
                    )

                    if not last_checkin or last_checkin[0]["log_type"] != log_type:
                        if settings.employee_checkin:
                            frappe.get_doc({
                                "doctype": "Employee Checkin",
                                "employee": employee_name,
                                "time": self.logdatetime,
                                "log_type": log_type,
                                "attendance_biometric": self.name
                            }).insert(ignore_permissions=True)

                # Check for duplicate Attendance
                attendance_exists = frappe.db.exists(
                    "Attendance",
                    {
                        "employee": employee_name,
                        "attendance_date": self.logdatetime,
                        "custom_time": self.logdatetime,
                        "company": "8848 Digital LLP",
                        "status": "Present"
                    }
                )

                if not attendance_exists:
                    last_attendance = frappe.get_all(
                        "Attendance",
                        filters={
                            "employee": employee_name,
                            "custom_time": ["<", self.logdatetime]
                              
                        },
                        fields=["custom_log_type"],
                        order_by="custom_time desc",
                        limit=1
                    )

                    if not last_attendance or last_attendance[0]["custom_log_type"] != log_type:
                        if settings.attendance:
                            frappe.get_doc({
                                "doctype": "Attendance",
                                "employee": employee_name,
                                "attendance_date": self.logdatetime,
                                "company": "8848 Digital LLP",
                                "status": "Present",
                                "attendance_biometric": self.name,
                                "custom_time": self.logdatetime,
                                "custom_log_type": log_type
                            }).insert(ignore_permissions=True)

                # Check for duplicate Attendance Request
                attendance_request_exists = frappe.db.exists(
                    "Attendance Request",
                    {
                        "employee": employee_name,
                        "from_date": logdatetime,
                        "to_date": logdatetime,
                        "custom_time": self.logdatetime,
                        "custom_log_type": log_type
                    }
                )

                if not attendance_request_exists:
                    last_request = frappe.get_all(
                        "Attendance Request",
                        filters={
                            "employee": employee_name,
                            "custom_time": ["<", self.logdatetime]
                              
                        },
                        fields=["custom_log_type"],
                        order_by="custom_time desc",
                        limit=1
                    )

                    if not last_request or last_request[0]["custom_log_type"] != log_type:
                        if settings.attendance_request:
                            frappe.get_doc({
                                "doctype": "Attendance Request",
                                "employee": employee_name,
                                "from_date": logdatetime.date(),
                                "to_date": logdatetime.date(),
                                "reason": "On Duty",
                                "status": "Present",
                                "attendance_biometric": self.name,
                                "custom_time": self.logdatetime,
                                "custom_log_type": log_type
                            }).insert(ignore_permissions=True)

            # Log success if error logging is enabled
            if settings.attendance_biometric_error_log:
                frappe.get_doc({
                    "doctype": "Attendance Biometric Error Log",
                    "title": "Success in AttendanceBiometric",
                    "time_stamp": now_datetime(),
                    "details": "AttendanceBiometric processed successfully"
                }).insert(ignore_permissions=True)

        except Exception as e:
            # Log error if error logging is enabled
            if settings.attendance_biometric_error_log:
                frappe.get_doc({
                    "doctype": "Attendance Biometric Error Log",
                    "title": "Error in AttendanceBiometric",
                    "time_stamp": now_datetime(),
                    "details": str(e)
                }).insert(ignore_permissions=True)
            frappe.log_error(message=str(e), title="Attendance Biometric Error")

        finally:
            # Commit changes to the database
            frappe.db.commit()
