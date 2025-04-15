// Copyright (c) 2025, sammish.thundiyil@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on("Datacenter", {
	refresh: function(frm) {
        frm.add_custom_button('Check Connection', function () {
            frappe.call({
                method: "node.node.doctype.datacenter.datacenter.check_proxmox_connection",
                args: {
                    docname: frm.doc.name
                },
                callback: function (r) {
                    if (r.message) {
                        frappe.msgprint({
                            title: __('Connection Status'),
                            message: r.message.message,
                            indicator: r.message.status === 'error' ? 'red' : 'green'
                        });
                        frm.reload_doc();
                    } else {
                        frappe.msgprint(__('No response received from server.'));
                    }
                },
                error: function (err) {
                    console.error("💥 API call failed:", err);
                    frappe.msgprint(__('There was an error calling the connection check. Check console for details.'));
                }
            });
        });
    }
});