import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import nowdate
from datetime import timedelta


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

            print(f"Processing logdatetime: {logdatetime}")  # Debugging point

            for employee in employees:
                employee_name = employee["name"]

                existing_checkins = frappe.get_all(
                    "Employee Checkin",
                    filters={"employee": employee_name, "time": ["<=", logdatetime]},
                    fields=["log_type"],
                    order_by="time asc",
                    limit=1
                )
                log_type = "IN" if not existing_checkins else "OUT" if logdatetime.hour >= 12 else "IN"
                print(f"Log type determined: {log_type}")  # Debugging point

                checkin_exists = frappe.db.exists(
                    "Employee Checkin",
                    {
                        "employee": employee_name,
                        "log_type": log_type,
                        "time": logdatetime
                    }
                )
                if not checkin_exists and settings.employee_checkin:
                    frappe.get_doc({
                        "doctype": "Employee Checkin",
                        "employee": employee_name,
                        "time": logdatetime,
                        "log_type": log_type,
                        "attendance_biometric": self.name,
                        "device_id": self.devicecode
                    }).insert(ignore_permissions=True)

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

                if settings.attendance_request:
                    today = nowdate()
                    existing_biometric_data = frappe.get_all(
                        "Attendance Biometric",
                        filters={
                            "devicecode": self.devicecode,
                            'creation': ['>=', today]
                        },
                        fields=["name"],
                        order_by="creation asc",
                    )
                    existing_biometric_data_end = frappe.get_all(
                        "Attendance Biometric",
                        filters={
                            "devicecode": self.devicecode,
                            'creation': ['>=', today]
                        },
                        fields=["name"],
                        order_by="creation desc",
                    )
                    if existing_biometric_data and existing_biometric_data_end:
                        start = existing_biometric_data[0]
                        end = existing_biometric_data_end[0]
                        start_biometric_record = frappe.get_doc("Attendance Biometric", start.get("name"))
                        end_biometric_record = frappe.get_doc("Attendance Biometric", end.get("name"))
                        
                        start_time = start_biometric_record.get("logdatetime")
                        end_time = end_biometric_record.get("logdatetime")
                        time_difference = end_time - start_time
                        print(time_difference)

                        if time_difference > timedelta(hours=4):
                            emp_logdatetime = end_biometric_record.get("logdatetime").strftime("%Y-%m-%d %H:%M:%S")
                            end_log_type = "OUT"
                            self.create_or_update_attendance_request(employee_name, emp_logdatetime, end_log_type, time_difference)
                        else:
                            emp_logdatetime = start_biometric_record.get("logdatetime").strftime("%Y-%m-%d %H:%M:%S")
                            start_log_type = "IN"
                            self.create_or_update_attendance_request(employee_name, emp_logdatetime, start_log_type, time_difference)
            
        except Exception as e:
            frappe.log_error(message=str(e), title="Attendance Biometric Error")
            print(f"Error: {str(e)}")  # Debugging point
        finally:
            frappe.db.commit()

    def create_or_update_attendance_request(self, employee_name, logdatetime, log_type, time_difference):
        """Helper function to create or update an attendance request."""
        
        if isinstance(logdatetime, str):
            logdatetime = datetime.strptime(logdatetime, "%Y-%m-%d %H:%M:%S")

        existing_attendance_request = frappe.get_all(
            "Attendance Request",
            filters={
                "employee": employee_name,
                "from_date": ["<=", logdatetime.date()],
                "to_date": [">=", logdatetime.date()],
                "company": "8848 Digital LLP"
            },
            fields=["name", "start_time", "end_time"]
        )

        print(f"Existing Attendance Requests: {existing_attendance_request}")  # Debugging point
        if existing_attendance_request and log_type == "OUT":
            attendance_request = existing_attendance_request[0]
            doc = frappe.get_doc("Attendance Request", attendance_request["name"])
            doc.end_time = logdatetime
            doc.custom_log_type = log_type
            doc.custom_total_working_hours = time_difference
            if time_difference < timedelta(hours=5):
                today = nowdate()
                doc.half_day = 1
                doc.half_day_date = today
            else:
                doc.half_day = 0
                doc.half_day_date = None
            doc.save(ignore_permissions=True)
        elif log_type == "IN":
            frappe.get_doc({
                "doctype": "Attendance Request",
                "employee": employee_name,
                "from_date": logdatetime.date(),
                "to_date": logdatetime.date(),
                "company": "8848 Digital LLP",
                "start_time": logdatetime.time(),
                "end_time": None,
                "custom_time": logdatetime,
                "custom_log_type": log_type,
                "reason": "On Duty",
                "attendance_biometric": self.name,
                "custom_created_by_attendance_biometric": 1
            }).insert(ignore_permissions=True)
