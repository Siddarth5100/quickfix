# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobCard(Document):
    def validate(self):
        print("VALIDATE RUNNING")
        print("controller validate running")

        '''
        Dangerous patterns: TWO bugs related to document lifecycle
        '''
        # bug 1
        '''
        self.parts_total = sum(r.total_price for r in self.parts_used)
        print(self.parts_used)
        self.save()
        '''

        #  bug 2
        '''
        for part in self.parts_used:
            other = frappe.get_doc("Spare Part", part.part)
            print("1---------bug fix: other", other)
            other.stock_qty -= part.quantity
            other.save()
        frappe.throw("Inconsistent error")
        '''
       
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

    def before_print(self, print_settings=None):
        self.print_summary = f"Name: {self.customer_name} - Brand: {self.device_brand} Model:{self.device_model}"
    

    def before_submit(self):
        # Only allow if status == "Ready for Delivery"
        if self.status != "Ready For Delivery":
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

    
        # print("publish realtime -------------")
        # frappe.publish_realtime()
        frappe.publish_realtime(
            "job_ready",
            {
                "job_card": self.name,
                "message": f"Job card {self.name} is ready!" 
            },
            user = self.owner
        )
        # print(f"realtime is published to owner", self.owner)
        '''
        Enqueue send_job_ready_email using frappe.enqueue - do NOT block the submit
        with a synchronous email send
        '''

        frappe.enqueue(
            method="quickfix.utils.send_job_ready_email",
            docname=self.name, 
            queue="short",
            timeout=300
        )
        

    def on_cancel(self):
        # Set status = "Cancelled"
        self.status = "Cancelled"

        #  restore stock
        for part in self.parts_used:
            print("----parrt", part.part)
            current_qty = frappe.db.get_value(
                "Spare Part", 
                part.part, 
                "stock_qty"
            )
            print("------crntqty--", current_qty, "part quan", part.quantity)

            frappe.db.set_value(
                "Spare Part",
                part.part,
                "stock_qty",
                current_qty + part.quantity
            )

        # cancel service invoice
        service_invoice = frappe.get_value(
            "Service Invoice",
            {"job_card": self.name},
        )
        
        print("-----------si", service_invoice)
        if service_invoice:
            invoice = frappe.get_doc("Service Invoice", service_invoice)
            
            if invoice.docstatus == 1:
                invoice.cancel()
            else:
                print(f"Invoice {invoice.name}")
        
        frappe.enqueue(
            method="quickfix.utils.send_job_cancel_email",
            docname=self.name, 
            queue="short",
            timeout=300
        )

    def on_trash(self):
        if self.status not in ["Cancelled", "Draft"]:
            frappe.throw(f"Status in {self.status}, can't delete ")

'''
# Task B - Multiple handler conflict:
def jobcard_validate(doc, method):
    frappe.msgprint("Hadler 1 ran")

'''

# F5 - Fixtures & Property Setters in Install
def after_install():
    print("Property setter printing------------")
    frappe.make_property_setter({
        "doctype": "Job Card",
        "field": "remarks",
        "property": "bold",
        "value": 1,
        "property_type": "Check"
    }    
)

# F2 - Install, Boot & Session Hooks
def before_uninstall():
    if frappe.db.exists("Job Card", {"docstatus": 1}):    
        frappe.throw("Submitted job card exisit, can't uninstall app")
