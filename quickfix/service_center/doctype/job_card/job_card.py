# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		# Validate customer_phone is exactly 10 digits
		if len(self.customer_phone) > 10:
			frappe.throw("customer number must be exactly 10 digits")

		# to check is the input is number
		for num in self.customer_phone:
			if not num.isdigit():
				frappe.throw("Enter only number")

		# If status is "In Repair" or beyond, assigned_technician must exist
		if self.status == "In Repair":
			if not self.assigned_technician:
				frappe.throw("Technician must exist")

		# calculate part usage entry(total price)
		# Compute each Part Usage Entry row: total_price = quantity × unit_price
		for each_row in self.parts_used:
			each_row.total_price = each_row.unit_price * each_row.quantity
		
		# Compute parts_total = sum of all row total_prices
		parts_total = 0

		for each_row in self.parts_used:
			parts_total = parts_total + each_row.total_price

		self.parts_total = parts_total
	
		# Set final_amount = parts_total + labour_charge
		if not self.labour_charge:
			rate = frappe.get_single('Settings')
			self.labour_charge = rate.default_labour_charge
		
		self.final_amount = self.parts_total + self.labour_charge
	
	def before_submit(self):
		# Only allow if status == "Ready for Delivery"
		if self.status != "Ready For Delivery":
			frappe.throw("Product status is not ready for delivery")

		# For each part in parts_used: check stock_qty >= quantity using frappe.db.get_value.
		# Throw a clear per-part error if not.		
		for each_part in self.parts_used:
			print("-----------stock", each_part.part, each_part.part_name, each_part.quantity, each_part.total_price)
			
			check_stock_qty = frappe.db.get_value(
				'Spare Part', 
				each_part.part, 
				'stock_qty')

			print("------stck_qty-------", check_stock_qty)
			if check_stock_qty < each_part.quantity:
				frappe.throw(
					f"Not enough stock for {each_part.part}. "
					f"Availble: {check_stock_qty}, Required: {each_part.quantity}"
				)

	def on_cancel(self):
		# Set status = "Cancelled"
		self.status = "Cancelled"
		