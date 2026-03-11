# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DeviceType(Document):
	pass

def after_install():
	# count = frappe.db.count('Device Type', 
	# 	{'device_type':""}
	# )

	# if count < 3:

	# 	name = frappe.db.exists('Device Type',
	# 		{'name': }
	# 	)

	# 	if name:
	# 		pass

	# 	frappe.new_doc()

	# device_types = ["Mac", "Tablet", "Laptop", "Smart Phones"]

	# for device in device_types:
	# 	device_exists = frappe.db.exists("Device Type",
	# 		{
	# 			"device_type": device
	# 		}
	# 	)

	# 	if not device_exists:
	# 		add_device = frappe.new_doc("Device Type")
	# 		add_device.device_type = device
	# 		if device == "Mac":
	# 			add_device.description = "MAC repair"
	# 			add_device.average_repair_hours = 2

	# frappe.msgprint("--------------Device Type created successfully")
		pass