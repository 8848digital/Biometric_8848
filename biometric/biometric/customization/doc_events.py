# import frappe

import frappe
def before_save(doc ,method = None):
    update_start_and_end_time(doc)
    

def update_start_and_end_time(doc):
    if doc.custom_created_by_attendance_biometric == 1:
        if doc.custom_log_type == "IN":
            # frappe.db.set_value(doc.doctype,doc.name,"end_time",None)
            doc.end_time = None
            
        

        


