# your_app/api.py

import frappe
from frappe import _

@frappe.whitelist()
def get_regions():
	return frappe.get_all("Region", fields=["name"])

@frappe.whitelist()
def get_servers_by_region(region):
	return frappe.get_all("Server", filters={"region": region}, fields=["name"])

@frappe.whitelist()
def get_node():
	return frappe.get_all("Node", fields=["name"])

@frappe.whitelist()
def get_node():
	return frappe.get_all("Node", fields=["name"])