# Copyright (c) 2025, sammish.thundiyil@gmail.com and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document

class Region(Document):
	pass

@frappe.whitelist()
def sync_regions_from_api():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    countries = response.json()

    for country in countries:
        continent = country.get('region')
        capital = country.get('capital', [''])[0]
        flag_url = country.get('flags', {}).get('png')  # <-- extract flag PNG
        country_name = country.get('name', {}).get('common')

        if capital and continent:
            if not frappe.db.exists("Region", {"region_name": capital}):
                doc = frappe.get_doc({
                    "doctype": "Region",
                    "region_name": capital,
                    "continent": continent,
                    "flag": flag_url  # <-- save URL to image field
                })
                doc.insert(ignore_permissions=True)


@frappe.whitelist()
def get_all_regions():
    return frappe.get_all("Region", fields=["region_name", "continent"])

@frappe.whitelist()
def get_regions_with_datacenters():
    regions = frappe.db.sql("""
        SELECT DISTINCT r.region_name, r.continent
        FROM `tabRegion` r
        JOIN `tabServer` s ON s.region = r.name
    """, as_dict=True)

    return regions
