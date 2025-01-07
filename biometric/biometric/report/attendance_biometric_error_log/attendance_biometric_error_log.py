import frappe
from frappe import _
import json
from datetime import datetime

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "employee_name", "label": _("Employee Name"), "fieldtype": "Data", "width": 150},
        {"fieldname": "employee_first_name", "label": _("First Name"), "fieldtype": "Data", "width": 150},
        {"fieldname": "log_date_time", "label": _("Log Date Time"), "fieldtype": "Datetime", "width": 150},
        {"fieldname": "log_date", "label": _("Log Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "log_time", "label": _("Log Time"), "fieldtype": "Time", "width": 100},
        {"fieldname": "employee_code", "label": _("Employee Code"), "fieldtype": "Data", "width": 150},
        {"fieldname": "device_code", "label": _("Device Code"), "fieldtype": "Data", "width": 100},
        {"fieldname": "direction", "label": _("Direction"), "fieldtype": "Data", "width": 100},
        {"fieldname": "download_date_time", "label": _("Download Date Time"), "fieldtype": "Datetime", "width": 150},
        {"fieldname": "title", "label": _("Title"), "fieldtype": "Data", "width": 200},
        {"fieldname": "create_attend_req", "label": _("Attendance Request"), "fieldtype": "Data", "width": 200},
    ]

def get_data(filters):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    employee_name = filters.get("employee_name")
    direction_filter = filters.get("direction")


    filter_conditions = {}

    if from_date and not to_date:
        filter_conditions["time_stamp"] = [">=", from_date]

    if to_date and not from_date:
        filter_conditions["time_stamp"] = ["<=", from_date]

    if from_date and to_date:
        filter_conditions["time_stamp"] = ["between", [from_date, to_date]]

    logs = frappe.get_all(
        "Attendance Biometric Error Log",
        filters=filter_conditions,
        fields=["title", "time_stamp", "details"],
        limit_page_length=1000
    )

    # Process data and split details
    data = []
    for log in logs:
        details_raw = log.get("details")
        
        # Check if details is None or not a valid JSON string
        if not details_raw:
            details = {}
        else:
            try:
                details = json.loads(details_raw)
            except json.JSONDecodeError:
                frappe.log_error(f"Invalid JSON in details for log {log['title']}: {details_raw}", "Attendance Biometric Error Log")
                details = {}

        master_attendance = details.get("MasterAttendance", {})
        device_code = master_attendance.get("DeviceCode")

        # Fetch employee details where attendance_device_id matches DeviceCode
        employee = frappe.db.get_value(
            "Employee",
            {"attendance_device_id": device_code},
            ["name", "first_name"],
            as_dict=True
        ) or {}

        # Determine direction based on AM/PM in log_date_time
        log_date_time = master_attendance.get("LogDateTime")
        direction = ""
        if log_date_time:
            try:
                log_datetime_obj = datetime.strptime(log_date_time, "%Y-%m-%d %H:%M:%S")
                if log_datetime_obj.hour < 12:
                    direction = "IN"
                else:
                    direction = "OUT"
            except ValueError:
                direction = "Unknown"
        master_data = {
            "title": log["title"],
            "employee_code": master_attendance.get("EmployeeCode"),
            "device_code": device_code,
            "log_date_time": log_date_time,
            "log_date": master_attendance.get("LogDate"),
            "log_time": master_attendance.get("LogTime"),
            "direction": direction,
            "download_date_time": master_attendance.get("DownloadDateTime"),
            "employee_name": employee.get("name"),
            "employee_first_name": employee.get("first_name"),
        }
        if employee_name and direction_filter:
            if (employee_name == employee.get("name")) and (direction_filter == direction):
                data.append(master_data)
        elif employee_name and employee_name == employee.get("name"):
            data.append(master_data)
        elif direction_filter and direction_filter == direction:
            data.append(master_data)
        elif not employee_name and not direction_filter:
            data.append(master_data)

    return data

from datetime import datetime

import frappe
from frappe.model.document import Document

from datetime import datetime

@frappe.whitelist(allow_guest=True)
def create_attendance_request(**kwargs):
    print("kwargs", kwargs)
    
    employee = kwargs.get("employee")
    from_date = kwargs.get("from_date")
    to_date = kwargs.get("to_date")
    custom_time = kwargs.get("custom_time")  
    start_time = kwargs.get("start_time") 
    end_time = kwargs.get("end_time") 
    custom_log_type = kwargs.get("custom_log_type")
    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")  # Assuming from_date is in "YYYY-MM-DD HH:MM:SS" format
    
    if from_date_obj.hour < 12:
        custom_log_type = "IN"
    else:
        custom_log_type = "OUT"
    attendance_request = frappe.new_doc('Attendance Request')
    attendance_request.employee = employee
    attendance_request.from_date = from_date
    attendance_request.to_date = to_date
    attendance_request.company = "8848 Digital LLP"
    attendance_request.custom_time = custom_time
    attendance_request.start_time = start_time
    attendance_request.end_time = end_time

    attendance_request.save()
    frappe.db.commit()

   
