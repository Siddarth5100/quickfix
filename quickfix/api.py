import frappe

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
