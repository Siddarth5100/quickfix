import frappe
from frappe.utils import today
import time

def test_bg_job():
    frappe.logger().info("BG Job executed")
    print("---------------Bg Job Executed")

# K1 Task A - Queue names:

'''
Enqueue send_job_ready_email on "short" queue (quick email, must not wait behind
heavy jobs)
'''
def send_job_ready_email(docname):
    print("---docname", docname)
    job_card = frappe.get_doc("Job Card", docname)
    print("jobcard", job_card)

    frappe.sendmail(
        recipients=job_card.customer_email,
        subject=f"Your Job Card {job_card.name} is ready",
        message=f"Hello {job_card.customer_name}, Your device: {job_card.device_type} is ready"
    )

    print(f"Email sent to {job_card.customer_email}")

#  for practice if user cancelled will send a mail
def send_job_cancel_email(docname):
    print("---docname", docname)

    job_card = frappe.get_doc("Job Card", docname)
    print("--jobcard", job_card)

    frappe.sendmail(
        recipients=job_card.customer_email,
        subject=f"Your Job card {job_card.name}, is cancelled",
        message=f"Hello {job_card.customer_name}, your Job Card {job_card.name}, got cancelled" 
    )

# Task B - Idempotency:
'''
The daily low-stock-check job can accidentally run twice if the scheduler misfires.
Make it idempotent:

def check_low_stock():
# Idempotency guard: check if already run today last_run = frappe.db.get_value("Audit Log",
{"action":"low_stock_check","date":today()}, "name")
if last_run: return # already ran today, skip # ... rest of job
'''

def check_low_stock():
    print("Running low stock check")

    last_run = frappe.db.get_value(
        "Audit Log",
        {
            "action": "low_stock_check",
            "creation": ["like", f"{today()}%"]
        },
        "name"
    )

    if last_run:
        print("Already ran today, skipping...")
        return

    print("Checking low stock item")

    frappe.get_doc({
        "doctype": "Audit Log",
        "action": "low_stock_check",
        "doctype_name": "Item"
    }).insert(ignore_permissions=True)

# Task C - Long-running job with progress updates:
def generate_monthly_revenue_report(year=None):
    months = range(1, 13)
    for i, month in enumerate(months, 1):
        time.sleep(1) #testing purpose

        revenue = frappe.get_list(
            "Job Card",
            filters={
                "status": "Delivered"
            },
        )

        frappe.publish_progress(
            percent=round(i/12*100),
            title="Generating Revenue Report",
            description=f"Processing month {month}"
        )

        print(f"Month {month}")
        # raise Exception("Test failure")

def extend_bootinfo(bootinfo):
    settings = frappe.get_single("Settings")
    
    bootinfo.quickfix_shop_name = settings.shop_name
    bootinfo.quickfix_manager_email = settings.manager_email

# K2 - Scheduler Events & Cron
def low_stock():
    stock_qty_check = frappe.get_all(
        "Spare Part",
        fields=['stock_qty', 'reorder_level']
    )

    for item in stock_qty_check:
        stock = item.get('stock_qty')
        reorder = item.get('reorder_level')

        if stock <= reorder:
            print("Low stock alert")