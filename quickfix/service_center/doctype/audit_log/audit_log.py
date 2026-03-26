# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class AuditLog(Document):
	pass

# Task A - Wildcard handler:
# Add a wildcard doc_events entry that logs every save of every DocType
# Registered dotted path in the hooks file
def log_change(doc, method):
	# to avoid recursive error(without this it is creating audit log too and running like loop)	
	if doc.doctype == "Audit Log":
		return

	frappe.get_doc({
		"doctype": 'Audit Log',
		"doctype_name": doc.doctype,
		"document_name": doc.name,
		"action": method,
		"user": frappe.session.user,
		"timestamp": now_datetime()
	}).insert()

def log_user_session(user, method="Login"):
    frappe.get_doc({
        "doctype": "Audit Log",
		"doctype_name": "User Session",
		"document_name": user,
		"action": method,
        "user": user,
		"timestamp": frappe.utils.now_datetime()
    }).insert(ignore_permissions=True)

