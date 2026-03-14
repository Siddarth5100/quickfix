# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": "Part Name",
			"fieldname": "part_name",
			"fieldtype": "Data"
		},
		{
			"label": "Part Code",
			"fieldname": "part_code",
			"fieldtype": "Data"
		},
		{
			"label": "Device Type",
			"fieldname": "device_type",
			"fieldtype": "Data"
		},
		{
			"label": "Stock Qty",
			"fieldname": "stock_qty",
			"fieldtype": "Int"
		},
		{
			"label": "Reorder Level",
			"fieldname": "reorder_level",
			"fieldtype": "Int"
		},
		{
			"label": "Unit Cost",
			"fieldname": "unit_cost",
			"fieldtype": "Currency"	
		},
		{
			"label": "Selling Price",
			"fieldname": "selling_price",
			"fieldtype": "Currency"
		},
		{
			"label": "Margin %",
			"fieldname": "margin",
			"fieldtype": "Int"
		}
	]

	return columns

def get_data(filters):
	data = []
	
	spare_parts_avail = frappe.get_all(
		'Spare Part',
		fields = [
			"part_name",
			"part_code",
			"compatible_device_type",
			"unit_cost",
			"selling_price",
			"stock_qty",
			"reorder_level"
		]
	)
	

	for parts in spare_parts_avail:
		row = {
			"part_name": parts.part_name,
			"part_code": parts.part_code,
			"device_type": parts.compatible_device_type,
			"unit_cost": parts.unit_cost,
			"selling_price": parts.selling_price,
			"stock_qty": parts.stock_qty,
			"reorder_level": parts.reorder_level
		}

		data.append(row)


	return data
