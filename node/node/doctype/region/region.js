// Copyright (c) 2025, sammish.thundiyil@gmail.com and contributors
// For license information, please see license.txt

frappe.ui.form.on('Region', {
	refresh: function (frm) {
		frappe.call({
            method: "node.node.doctype.region.region.sync_regions_from_api",
            callback: function () {
                frappe.msgprint("Regions synced successfully.");
            }
        });
	}
});


