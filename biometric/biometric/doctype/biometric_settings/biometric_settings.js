// Copyright (c) 2024, 8848 Digital and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Biometric Settings", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Biometric Settings", {
    refresh(frm) {
        frm.add_custom_button(__('Manually Fetch Attendance'), function() {
            frappe.call({
                method: 'biometric.biometric.api.essl.fetch_attendance.get_attendance_logs',
                callback: function(r) {
                    if (!r.exc) {
                        frappe.msgprint(__('Attendance logs fetched successfully.'));
                    }
                }
            });
        });
    },
});
