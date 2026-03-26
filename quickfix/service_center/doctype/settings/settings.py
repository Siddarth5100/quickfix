# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import time


class Settings(Document):
	pass

# Jinja hooks:
def get_shop_name():
	settings = frappe.get_single('Settings')

	return settings.shop_name

# Jinja hooks:
def prefix(value):
	prefix_format = "JOB#"

	return prefix_format+str(value)