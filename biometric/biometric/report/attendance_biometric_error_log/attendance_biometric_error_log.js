frappe.query_reports["Attendance Biometric Error Log"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
        },
        {
            "fieldname": "employee_name",
            "label": __("Employee Name"),
            "fieldtype": "Link",
            "options": "Employee",
        },
        {
            "fieldname": "direction",
            "label": __("Direction"),
            "fieldtype": "Select",
            "options": ["", "IN", "OUT"],
        }
    ],
    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        
        if (column.id == "create_attend_req") {
            // Create the button with a click event
            value = `<a class="btn-create-attend-req" 
                        style="margin-left:5px; border:none; color: #fff; background-color: #5E64FF; 
                        padding: 3px 5px; border-radius: 5px;" 
                        onclick="createAttendanceRequest('${data.employee_name}', '${data.log_date_time}','${data.log_date_time}','${data.direction}','${data.log_time}')">
                        Create Attendance Request</a>`;
        }
        return value;
    }
};

function createAttendanceRequest(employee_name, from_date, to_date, direction, log_time,log_date_time) {
    let logHour = new Date(log_time).getHours();
    let custom_log_type = (logHour < 12) ? "IN" : "OUT"; // Set IN for AM and OUT for PM

    frappe.call({
        method: "biometric.biometric.report.attendance_biometric_error_log.attendance_biometric_error_log.create_attendance_request",  // Replace with your actual path to the backend method
        args: {
            employee: employee_name,
            from_date: from_date,
            to_date: to_date,
            company: "8848 Digital LLP",
            custom_time: log_date_time,
            custom_log_type: custom_log_type,
            start_time: log_time ,
            end_time: log_time
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.msgprint(__('Attendance Request Created Successfully'));
                frappe.query_reports["Attendance Biometric Error Log"].get_data();
            } else {
                frappe.msgprint(__('Failed to create Attendance Request'));
            }
        }
    });
}
