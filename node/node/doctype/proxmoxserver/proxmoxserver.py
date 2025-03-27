# from proxmoxer import ProxmoxAPI

# ✅ Your Proxmox Server Details
host = "103.27.235.186"  # Your Proxmox Server IP
port = 8006
username = "root@pam"
auth_type = "Password"  # Change to "API Token" if using an API token
password = "RtG4#2%Sq!#&"  # Your Proxmox password (if using password authentication)
api_token_id = "mytokenid"  # Only needed if using API token
api_token_secret = "your-api-token-secret"  # Replace with your actual API token

# ✅ Construct URL
proxmox_url = f"https://{host}:{port}"

try:
    if auth_type == "API Token":
        proxmox = ProxmoxAPI(
            host,
            user=f"{username}!{api_token_id}",  # ✅ Correct API token format
            token_value=api_token_secret,
            verify_ssl=False
        )
    else:
        proxmox = ProxmoxAPI(
            host,
            user=username,
            password=password,
            verify_ssl=False
        )

    # ✅ Fetch Nodes
    nodes = proxmox.nodes.get()

    print(f"✅ Connection Successful!\n"
          f"🔹 Proxmox URL: {proxmox_url}\n"
          f"🔹 Username: {username}\n"
          f"🔹 Auth Type: {auth_type}\n"
          f"🔹 Nodes Available: {nodes}")

except Exception as e:
    print(f"❌ Connection Failed: {str(e)}")





# import frappe
# from proxmoxer import ProxmoxAPI

# @frappe.whitelist()
# def check_proxmox_connection(docname):
#     """Check Proxmox Connection when saving the Proxmox Server Doctype"""

#     # Fetch document details
#     doc = frappe.get_doc("Proxmox Server", docname)

#     url = doc.url
#     port = doc.port
#     username = doc.username
#     auth_type = doc.auth_type
#     api_token = doc.api_token
#     password = doc.password

#     try:
#         if auth_type == "API Token":
#             proxmox = ProxmoxAPI(
#                 url,
#                 user=username,
#                 token_value=api_token,  # No token ID required
#                 port=port,
#                 verify_ssl=False  # Change to True if using SSL
#             )
#         else:
#             proxmox = ProxmoxAPI(
#                 url,
#                 user=username,
#                 password=password,
#                 port=port,
#                 verify_ssl=False
#             )

#         # ✅ Fetch Proxmox Nodes
#         nodes = proxmox.nodes.get()

#         # ✅ Store success message in Frappe
#         doc.status = "Connected ✅"
#         doc.save()

#         return {
#             "status": "success",
#             "message": f"✅ Connection Successful!\n"
#                        f"🔹 Proxmox URL: {url}:{port}\n"
#                        f"🔹 Username: {username}\n"
#                        f"🔹 Auth Type: {auth_type}\n"
#                        f"🔹 Nodes Available: {nodes}"
#         }

#     except Exception as e:
#         # Store failure message in Frappe
#         doc.status = "Connection Failed ❌"
#         doc.save()

#         return {
#             "status": "error",
#             "message": f"❌ Connection Failed: {str(e)}"
#         }
