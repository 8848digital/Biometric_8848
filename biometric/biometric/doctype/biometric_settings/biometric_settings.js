frappe.ui.form.on("Biometric Settings", {
    refresh(frm) {
        frm.add_custom_button(__('Manually Fetch Attendance'), function() {
            if (!frm.doc.from_date || !frm.doc.to_date) {
                frappe.msgprint(__('Please set both From Date and To Date.'));
                return;
            }
            frappe.call({
                method: 'biometric.biometric.api.essl.fetch_attendance.get_attendance_logs',
                args: {
                    from_date: frm.doc.from_date,
                    to_date: frm.doc.to_date
                },
                callback: function(r) {
                    if (!r.exc) {
                        frappe.msgprint(__('Attendance logs fetched successfully.'));
                    }
                }
            });
        });
    },
});
