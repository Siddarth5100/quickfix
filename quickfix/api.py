import frappe

# whitelisted method to share the read access permission to specifix user
@frappe.whitelist()
def share_job_card(job_card_name, user_email):
    frappe.share.add(
        doctype= "Job Card",
        name= job_card_name,
        user= user_email,
        read= 1,
        write= 0,
        share= 0
    )

    return "shared successfully"

# for only manager role api
'''
If non-manager calls user will get PermissionError
'''
@frappe.whitelist(allow_guest = False)
def only_manager():
    frappe.only_for("QF Manager")

    return "Manager calls"

# In a utility function, call frappe.rename_doc("Technician", old_name, new_name,
# merge=False)
@frappe.whitelist()
def rename_technician(old_name, new_name):
    frappe.rename_doc(
        'Technician',
        old_name,
        new_name,
        merge= False        
    )
    
    frappe.db.commit()
    
    return {"status": f"Rename done from {old_name} to {new_name}"}

# B2 Part B: frappe.qb Query Builder (write in api.py)

'''
Write a function get_overdue_jobs() using frappe.qb (NOT frappe.db.sql) that:

Queries Job Card table
Filters: status IN ("Pending Diagnosis","In Repair") AND creation < now minus 7 days
Returns: name, customer_name, assigned_technician, creation
Orders by creation ASC
'''

@frappe.whitelist()
def get_overdue_jobs():
    job_card = frappe.qb.DocType("Job Card")

    query = (
	    frappe.qb.from_(job_card)
	    .select(
            job_card.name, 
            job_card.customer_name,
            job_card.assigned_technician,
            job_card.creation
        )
	    .where(
		    job_card.status.isin(["Diagnosis", "In Repair"])
	    )
	    .orderby(job_card.creation)
    )
    
    return query.run(as_dict=True)


'''
Write a function transfer_job(from_tech, to_tech) that reassigns all open Job Cards from one
technician to another. It must:

Use frappe.db.sql inside a try/except block
Call frappe.db.commit() only on success
Call frappe.db.rollback() in the except block
Log the exception with frappe.log_error before re-raising
'''

# @frappe.whitelist()
# def transfer_job(from_tech, to_tech):

#     try:
#         frappe.db.sql(
#             """
#             UPDATE `tabJob Card`
#             SET assigned_technician = %s
#             WHERE assigned_technician = %s
#             AND Status NOT IN ('Delivered', 'Cancelled')""", 
#             (to_tech, from_tech))

#         frappe.db.commit()

#         return "Transfer completed"
    
#     except Exception as e:
#         frappe.db.rollback()

#         frappe.log_error(frappe.get_traceback(), "Job Transfer failed")

#         raise

@frappe.whitelist()
def transfer_job(from_tech, to_tech):
    try:
        # single-line SQL string, backticks around table and column names
        sql = "UPDATE `tabJob Card` SET `assigned_technician` = %s WHERE `assigned_technician` = %s AND `Status` NOT IN ('Delivered', 'Cancelled')"
        
        frappe.db.sql(sql, (to_tech, from_tech))
        frappe.db.commit()
        return "Transfer completed"
    
    except Exception:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Job Transfer failed")
        raise