import frappe
from frappe.model.document import Document
from proxmoxer import ProxmoxAPI


class ProxmoxServer(Document):
    pass


@frappe.whitelist()
def check_proxmox_connection(docname):
    print("🔍 check_proxmox_connection CALLED with docname:", docname)

    # Fetch document
    doc = frappe.get_doc("Proxmox Server", docname)

    # Log and clean inputs
    print("📌 Raw doc.url:", doc.url)
    print("📌 Raw doc.port:", doc.port)
    print("📌 Raw doc.auth_type:", doc.auth_type)

    clean_url = doc.url.strip().replace("http://", "").replace("https://", "")
    base_url = clean_url  # no protocol at all

    port = int(str(doc.port).strip())  # ✅ Clean and convert port safely

    username = doc.user_name
    auth_type = doc.auth_type
    api_token = doc.api_token
    password = doc.password

    print("✅ Cleaned URL:", base_url)
    print("✅ Cleaned Port:", port)

    try:
        # Choose auth method
        if auth_type == "Api Token":
            print("🔐 Using API Token authentication")
            proxmox = ProxmoxAPI(
                base_url,
                user=username,
                token_value=api_token,
                port=port,
                verify_ssl=False
            )
        else:
            print("🔐 Using Password authentication")
            proxmox = ProxmoxAPI(
                base_url,
                user=username,
                password=password,
                port=port,
                verify_ssl=False
            )

        # Fetch Proxmox nodes
        nodes = proxmox.nodes.get()
        print("✅ Nodes fetched:", nodes)

        # ✅ Properly indented return inside try block
        return {
            "status": "success",
            "message": f"✅ Connection Successful!\n"
                       f"🔹 Proxmox URL: {base_url}:{port}\n"
                       f"🔹 Username: {username}\n"
                       f"🔹 Auth Type: {auth_type}\n"
                       f"🔹 Nodes Available:\n" + "\n".join([
                           f"   • Node: {n.get('node')}, Status: {n.get('status')}, CPU: {n.get('cpu')}, Memory: {n.get('mem')}"
                           for n in nodes
                       ])
        }

    except Exception as e:
        print("❌ Error occurred:", str(e))
        frappe.log_error(frappe.get_traceback(), "Proxmox Connection Failed")
        return {
            "status": "error",
            "message": f"❌ Connection Failed: {str(e)}"
        }
