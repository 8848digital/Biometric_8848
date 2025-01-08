from datetime import datetime
from frappe.utils import nowdate
from datetime import timedelta
import frappe
def before_save(doc, method=None):
    if doc.is_new():
        update_start_and_end_time(doc)
    # else:
    #     half_day_attendance_request(doc)

# def after_save(doc):
#     half_day_attendance_request(doc)
    
def update_start_and_end_time(doc):
    if doc.custom_created_by_attendance_biometric == 1:
        if doc.custom_log_type == "IN":
            doc.end_time = None

# def half_day_attendance_request(doc):
#     if doc.custom_created_by_attendance_biometric and (doc.custom_log_type == "OUT") and doc.start_time and doc.end_time:
#         today = nowdate()
#         time_format = '%H:%M:%S'
#         time_a = datetime.strptime(doc.start_time, time_format)
#         time_b = datetime.strptime(doc.end_time, time_format)

#         time_diff = time_b - time_a
#         if time_diff.total_seconds() > 4 * 3600:  # 4 hours in seconds
#             doc.half_day = 1
#             doc.half_day_date = today
