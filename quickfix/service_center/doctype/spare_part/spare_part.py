# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SparePart(Document):
	def validate(self):
		if self.selling_price <= self.unit_cost:
			frappe.throw("Selling price must be grater than unit cost")
