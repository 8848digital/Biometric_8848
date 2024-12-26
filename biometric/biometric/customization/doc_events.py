import frappe
def before_save(doc ,method = None):
    print("before_save11111111111111111111111111111")
    update_start_and_end_time(doc)
    

def update_start_and_end_time(doc):
    print("update_start_and_end_time111111111111111111111111111111",doc.created_by_attendance_biometric,doc.custom_log_type)
    if doc.created_by_attendance_biometric == 1:
        if doc.custom_log_type == "IN":
            # frappe.db.set_value(doc.doctype,doc.name,"end_time",None)
            doc.end_time = None
            
        

        


