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

    "onload": function(report) {
        // Adding a custom button to the report
        report.page.add_button(__("Create Attendance Request"), function() {
            // Functionality when button is clicked
            frappe.call({
                method: "your_custom_app.path.to.create_attendance_request_method",
                args: {
                    // Pass required parameters (filters or selected data from report)
                    "from_date": report.filters.from_date,
                    "to_date": report.filters.to_date,
                    "employee_name": report.filters.employee_first_name,
                    "direction": report.filters.direction
                },
                callback: function(response) {
                    if (response.message) {
                        frappe.msgprint(__('Attendance Request created successfully.'));
                    } else {
                        frappe.msgprint(__('Failed to create Attendance Request.'));
                    }
                }
            });
        });
    }
};
