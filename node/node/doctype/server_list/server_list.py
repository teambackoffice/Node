# Copyright (c) 2025, sammish.thundiyil@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from proxmoxer import ProxmoxAPI


class ServerList(Document):
    pass


@frappe.whitelist()
def check_proxmox_connection(docname):
    print("🔍 check_proxmox_connection CALLED with docname:", docname)

    doc = frappe.get_doc("Server List", docname)

    clean_url = doc.url.strip().replace("http://", "").replace("https://", "")
    base_url = clean_url
    port = int(str(doc.port).strip())

    username = doc.user_name
    auth_type = doc.auth_type
    api_token = doc.api_token
    password = doc.password

    try:
        # Connect to Proxmox API
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
                doc.status = "❌ No password provided"
                doc.save(ignore_permissions=True)
                return {
                    "status": "error",
                    "message": "❌ Password authentication selected, but no password provided."
                }
            proxmox = ProxmoxAPI(
                base_url,
                user=username,
                password=password,
                port=port,
                verify_ssl=False
            )

        nodes = proxmox.nodes.get()
        created_nodes = []
        iso_images = []
        vm_list = []

        if nodes:
            node_status = nodes[0].get("status")
            doc.status = node_status
            doc.save(ignore_permissions=True)

        for n in nodes:
            node_name = n.get("node")
            status = n.get("status")

            # Node insert/update
            try:
                if not frappe.db.exists("Node", node_name):
                    node_doc = frappe.get_doc({
                        "doctype": "Node",
                        "node": node_name,
                        "status": status
                    })
                    node_doc.insert(ignore_permissions=True)
                    created_nodes.append(f"✅ Created Node: {node_name} (Status: {status})")
                else:
                    existing = frappe.get_doc("Node", node_name)
                    existing.status = status
                    existing.save(ignore_permissions=True)
                    created_nodes.append(f"♻️ Updated Node: {node_name} (Status: {status})")
            except Exception as e:
                frappe.log_error(frappe.get_traceback(), f"Failed to create/update node: {node_name}")

            # ISO Image extraction and creation
            try:
                storage_list = proxmox.nodes(node_name).storage.get()
                for storage in storage_list:
                    if "content" in storage and "iso" in storage["content"]:
                        storage_id = storage["storage"]
                        iso_list = proxmox.nodes(node_name).storage(storage_id).content.get()
                        for item in iso_list:
                            if item.get("content") == "iso":
                                volid = item.get("volid")
                                iso_name = volid.split("/")[-1] if volid else None

                                if iso_name:
                                    iso_images.append(iso_name)

                                    if not frappe.db.exists("ISO Images", {"iso_image": iso_name}):
                                        iso_doc = frappe.get_doc({
                                            "doctype": "ISO Images",
                                            "iso_image": iso_name
                                        })
                                        iso_doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(frappe.get_traceback(), f"Failed to fetch ISOs for node: {node_name}")

            # VM List and Virtual Machine Doc creation
            try:
                vms = proxmox.nodes(node_name).qemu.get()
                for vm in vms:
                    vmid = vm.get("vmid")
                    name = vm.get("name") or f"VM-{vmid}"
                    vm_display = f"{vmid} ({name})"
                    vm_list.append(vm_display)

                    # Create Virtual Machine doc if not exists
                    if not frappe.db.exists("Virtual Machine", {"vm": vm_display}):
                        vm_doc = frappe.get_doc({
                            "doctype": "Virtual Machine",
                            "vm": vm_display
                        })
                        vm_doc.insert(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(frappe.get_traceback(), f"Failed to fetch VMs for node: {node_name}")

        return {
            "status": "success",
            "message": f"✅ Connection Successful!\n"
                       f"🔹 Proxmox URL: {base_url}:{port}\n"
                       f"🔹 Username: {username}\n"
                       f"🔹 Auth Type: {auth_type}\n"
                       f"🔹 Nodes Processed:\n" + "\n".join(created_nodes) + "\n\n"
                       f"📀 ISO Images:\n" + ("\n".join(iso_images) if iso_images else "No ISO images found.") + "\n\n"
                       f"🖥️ Virtual Machines:\n" + ("\n".join(vm_list) if vm_list else "No VMs found.")
        }

    except Exception as e:
        error_message = f"❌ offline"
        doc.status = error_message
        doc.save(ignore_permissions=True)
        frappe.log_error(frappe.get_traceback(), "Proxmox Connection Failed")
        return {
            "status": "error",
            "message": error_message
        }

@frappe.whitelist()
def get_servers_with_region_flags():
    return frappe.db.sql("""
        SELECT 
            s.name AS id,
            s.port,
            s.status,
            s.region,
            s.user_name,
            s.url,
            r.flag,
            r.region_name
        FROM `tabServer List` s
        LEFT JOIN `tabRegion` r ON r.region_name = s.region
    """, as_dict=True)
