import frappe

def test_bg_job():
    frappe.logger().info("BG Job executed")
    print("---------------Bg Job Executed")