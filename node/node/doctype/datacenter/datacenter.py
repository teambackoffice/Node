# Copyright (c) 2025, sammish.thundiyil@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from proxmoxer import ProxmoxAPI


class Datacenter(Document):
	pass

@frappe.whitelist()
def check_proxmox_connection(docname):
    print("🔍 check_proxmox_connection CALLED with docname:", docname)

    # Fetch document
    doc = frappe.get_doc("Datacenter", docname)

    # Clean URL and port
    clean_url = doc.url.strip().replace("http://", "").replace("https://", "")
    base_url = clean_url
    port = int(str(doc.port).strip())

    username = doc.user_name
    auth_type = doc.auth_type
    api_token = doc.api_token
    password = doc.password

    try:
        # Connect using appropriate auth
        if auth_type == "Api Token":
            proxmox = ProxmoxAPI(
                base_url,
                user=username,
                token_value=api_token,
                port=port,
                verify_ssl=False
            )
        else:
            if not password:
                return {"status": "error", "message": "❌ Password authentication selected, but no password provided."}
            proxmox = ProxmoxAPI(
                base_url,
                user=username,
                password=password,
                port=port,
                verify_ssl=False
            )

        # Fetch nodes
        nodes = proxmox.nodes.get()
        created_nodes = []

        for n in nodes:
            node_name = n.get("node")
            status = n.get("status")

            # Create or update Node document
            try:
                node_doc = frappe.get_doc({
                    "doctype": "Node",
                    "node": node_name,
                    "status": status
                })
                node_doc.insert(ignore_permissions=True)
                created_nodes.append(f"✅ Created Node: {node_name} (Status: {status})")
            except frappe.DuplicateEntryError:
                existing = frappe.get_doc("Node", node_name)
                existing.status = status
                existing.save(ignore_permissions=True)
                created_nodes.append(f"♻️ Updated Node: {node_name} (Status: {status})")

        return {
            "status": "success",
            "message": f"✅ Connection Successful!\n"
                       f"🔹 Proxmox URL: {base_url}:{port}\n"
                       f"🔹 Username: {username}\n"
                       f"🔹 Auth Type: {auth_type}\n"
                       f"🔹 Nodes Processed:\n" + "\n".join(created_nodes)
        }

    except Exception as e:
        print("❌ Error occurred:", str(e))
        frappe.log_error(frappe.get_traceback(), "Proxmox Connection Failed")
        return {
            "status": "error",
            "message": f"❌ Connection Failed: {str(e)}"
        }
