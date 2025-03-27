// frappe.ui.form.on('Proxmox Server', {
//     refresh: function(frm) {
//         frm.add_custom_button('Check Connection', function() {
//             frappe.call({
//                 method: "node.node.doctype.proxmoxserver.proxmoxserver.check_proxmox_connection",
//                 args: {
//                     docname: frm.doc.name
//                 },
//                 callback: function(r) {
//                     if (r.message) {
//                         frappe.msgprint(r.message.message);
//                         frm.reload_doc();
//                     }
//                 }
//             });
//         });
//     }
// });

