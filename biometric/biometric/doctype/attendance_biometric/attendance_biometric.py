import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from datetime import datetime

# Attendance Biometric
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
                                "attendance_biometric": self.name,
                                "device_id":self.devicecode
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

                existing_attendance_request = frappe.get_all(
                    "Attendance Request",
                    filters={
                        "employee": employee_name,
                        "from_date": ["<=", logdatetime.date()],
                        "to_date": [">=", logdatetime.date()],
                        "company": "8848 Digital LLP",
                    },
                    fields=["name", "start_time", "end_time"]
                )

                # Initialize start_time and end_time based on AM/PM
                start_time = None
                end_time = None

                if logdatetime.hour < 12:  # AM
                    start_time = logdatetime.time()
                else:  # PM
                    end_time = logdatetime.time()

                if existing_attendance_request:
                    # Update the existing Attendance Request
                    attendance_request = existing_attendance_request[0]  # Assuming only one request per day
                    doc = frappe.get_doc("Attendance Request", attendance_request["name"])
                    
                    # Update start_time if it's AM and not already set
                    if start_time and not doc.start_time:
                        doc.start_time = start_time
                    
                    # Update end_time if it's PM
                    if end_time:
                        doc.end_time = end_time
                    
                    # Update other fields if necessary
                    doc.custom_time = self.logdatetime
                    doc.custom_log_type = log_type
                    doc.reason = "On Duty"
                    doc.attendance_biometric = self.name
                    doc.custom_created_by_attendance_biometric = 1
                    
                    doc.save(ignore_permissions=True)
                else:
                    # Create a new Attendance Request if none exists
                    frappe.get_doc({
                        "doctype": "Attendance Request",
                        "employee": employee_name,
                        "from_date": logdatetime.date(),
                        "to_date": logdatetime.date(),
                        "company": "8848 Digital LLP",
                        "start_time": start_time,
                        "end_time": end_time,
                        "custom_time": self.logdatetime,
                        "custom_log_type": log_type,
                        "reason": "On Duty",
                        "attendance_biometric": self.name,
                        "custom_created_by_attendance_biometric": 1
                    }).insert(ignore_permissions=True)

            # if settings.attendance_biometric_error_log:
            #     frappe.get_doc({
            #         "doctype": "Attendance Biometric Error Log",
            #         "title": "Success in AttendanceBiometric",
            #         "time_stamp": now_datetime(),
            #         "details": "AttendanceBiometric processed successfully"
            #     }).insert(ignore_permissions=True)

        except Exception as e:
            # if settings.attendance_biometric_error_log:
            #     frappe.get_doc({
            #         "doctype": "Attendance Biometric Error Log",
            #         "title": "Error in AttendanceBiometric",
            #         "time_stamp": now_datetime(),
            #         "details": str(e)
            #     }).insert(ignore_permissions=True)
            frappe.log_error(message=str(e), title="Attendance Biometric Error")

        finally:
            frappe.db.commit()