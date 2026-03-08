# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class AuditLog(Document):
	pass

# Add a wildcard doc_events entry that logs every save of every DocType
def log_change(doc, method):	
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
