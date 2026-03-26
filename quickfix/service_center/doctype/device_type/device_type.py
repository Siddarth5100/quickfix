# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DeviceType(Document):
	pass

# F2 - Install, Boot & Session Hook
# want to check this
def after_install():
	default_device_type = ['Tablet', 'Laptop', 'Smart Phones']

	device_count = frappe.db.count('Device Type')

	if device_count < 3:
		for device in default_device_type:
			if not frappe.db.exists('Device Type', device):
				frappe.get_doc({
					'doctype': 'Device Type',
					'device_type': device
				}).insert(ignore_permissions=True)	
	
	if not frappe.db.exists('Settings'):
		frappe.get_doc({
			'doctype': 'Settings',
			'shop_name': 'QuickFix',
			'default_labour_charge': 1000
		}).insert(ignore_permissions=True)	

	frappe.msgprint("Default setup done")