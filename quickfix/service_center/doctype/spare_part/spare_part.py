# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class SparePart(Document):
	def validate(self):
		if self.selling_price <= self.unit_cost:
			frappe.throw("Selling price must be grater than unit cost")

	# E2 autoname rename
	def autoname(self):
		# implement autoname()
		self.name = make_autoname("SP-.####")
		
		# convert part code to capital
		if not self.part_code:
			frappe.throw("Part code is empty!")

		self.part_code= self.part_code.upper()
		