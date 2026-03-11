import frappe
from quickfix.service_center.doctype.job_card.job_card import JobCard

class CustomJobCard(JobCard):
    def validate(self):
        super().validate()
        print("Custom Validation")
        self._check_urgent_unassigned()
        

    def _check_urgent_unassigned(self):
        if self.priority == "Urgent" and not self.assigned_technician:
            frappe.throw("Technician not assigned for Priority Urgent")
    
# MRO = method resolution order
'''
MRO: Method Resolution Order
* Is the order in which Python search classess to find a method when we call it.
* When we call a method, Python checks which class should run that method
'''

# super() is non-negotiable
'''
super(): When we are doing override like validate class from the core,
we should not leave super(), because the core validations will not run,
only what we written in child class that will run, based on the situation
will use super()
'''