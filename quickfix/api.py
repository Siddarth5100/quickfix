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
