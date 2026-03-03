# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		# Validate customer_phone is exactly 10 digits
		if len(self.customer_phone) > 10:
			# print("----------------------------",type(self.customer_phone))
			frappe.throw("customer number must be exactly 10 digits")

		# to check is the input is number
		for num in self.customer_phone:
			# print("-------------num", num)
			# if not num.isdigit():
			# 	print("No", num)
			# else:
			# 	print("Yes", num)
			if not num.isdigit():
				frappe.throw("Enter only number")

		if self.status == "In Repair":
			if not self.assigned_technician:
				frappe.throw("Technician must exist")