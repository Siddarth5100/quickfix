# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
	def validate(self):
		print("VALIDATE RUNNING")
		print("controller validate running")

		# Validate customer_phone is exactly 10 digits
		if len(self.customer_phone) > 10:
			frappe.throw("customer number must be exactly 10 digits")

		# to check is the input is number
		for num in self.customer_phone:
			if not num.isdigit():
				frappe.throw("Enter only number")

		# If status is "In Repair" or beyond, assigned_technician must exist
		if self.status in ["In Repair", "Ready For Delivery", "Delivered"]:
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
	
		# explore
		if not self.customer_email or not self.customer_email.strip():
			frappe.throw("Enter Mail-id")

	def before_submit(self):
		# Only allow if status == "Ready for Delivery"
		if not self.status == "Ready For Delivery":
			frappe.throw("Product status is not ready for delivery")

		# For each part in parts_used: check stock_qty >= quantity using frappe.db.get_value.
		# Throw a clear per-part error if not.		
		for each_part in self.parts_used:
			# print("-----------stock", each_part.part, each_part.part_name, each_part.quantity, each_part.total_price)
			
			check_stock_qty = frappe.db.get_value(
				'Spare Part', 
				each_part.part, 
				'stock_qty')

			# print("------stck_qty-------", check_stock_qty)
			if check_stock_qty < each_part.quantity:
				frappe.throw(
					f"Not enough stock for {each_part.part}. "
					f"Availble: {check_stock_qty}, Required: {each_part.quantity}"
				)
				
	def on_submit(self):
		# deduct stck qty for each part
		# if self.docstatus == 1:
		for qty in self.parts_used:
			
			avail_stock_qty = frappe.get_value(
				'Spare Part',
				qty.part,
				'stock_qty'
			)
		
			updated_stck = avail_stock_qty - qty.quantity

			frappe.db.set_value(
				'Spare Part',
				qty.part,
				'stock_qty',
				updated_stck,
			)

		# auto create service invoice
		frappe.get_doc({
			'doctype': 'Service Invoice',
			'job_card': self.name,
			'customer_name': self.customer_name,
			'labour_charge': self.labour_charge,
			'parts_total': self.parts_total,
			'total_amount': self.final_amount,
			'payment_status': "Unpaid"
		}).insert(ignore_permissions= True)
		# print("-----------test",doc, doc.job_card, doc.customer_name, doc.labour_charge)

	"""
		# frappe.publish_realtime()
		frappe.publish_realtime(
			"job_ready",
			{
				"job_card": self.name,
				"message": "Job is working" 
			},
			user = self.owner
		)
	"""
	# Enqueue send_job_ready_email using frappe.enqueue - do NOT block the submit
	# with a synchronous email send
	
	
	# def send_job_ready_email(job_card_name):
	# 	print("--------name", job_card_name)
	# 	job_card = frappe.get_doc(
	# 		'Job Card',
	# 		job_card_name
	# 	)
		
	# 	print("-----get_---", job_card, job_card.device_type)

	# frappe.enqueue(
	# 	method= send_job_ready_email,
	# 	queue= "short"
	# )


	def on_cancel(self):
		# Set status = "Cancelled"
		self.status = "Cancelled"

		#  restore stock
		
	def on_trash(self):

		if self.status not in ["Cancelled", "Draft"]:
			frappe.throw(f"Status in {self.status}, can't delete ")


def controller_test(doc, method):
	print("Hook validate triggered")
	print(doc.name, method)
	frappe.throw("Controller  Validation error")

print("Test print from controller, outside class through hooks")

# to test task b 2nd que


def wildcard_validate(doc, method):
	print("Wildcard validate:", doc.doctype)

def jobcard_validate(doc, method):
	print("Specific job card validate:", doc.name)
