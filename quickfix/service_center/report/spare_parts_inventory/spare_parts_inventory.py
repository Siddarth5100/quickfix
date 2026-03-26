# Copyright (c) 2026, Siddarth and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = get_columns(filters)
	data, report_summary = get_data(filters)

	return columns, data, None, None, report_summary

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
			"fieldtype": "Float"
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

	total_parts = 0
	below_reorder = 0
	total_value = 0
	total_stock_qty = 0

	for parts in spare_parts_avail:

		if parts.unit_cost:
			unit_cost = round(parts.unit_cost, 2)
		
		else:
			unit_cost = 0

		if parts.selling_price:
			selling_price = round(parts.selling_price, 2)

		else:
			selling_price = 0
		
		row = {
			"part_name": parts.part_name,
			"part_code": parts.part_code,
			"device_type": parts.compatible_device_type,
			"unit_cost": unit_cost,
			"selling_price": selling_price,
			"stock_qty": parts.stock_qty,
			"reorder_level": parts.reorder_level
		}
		
		# summary updates
		total_parts += 1

		if parts.stock_qty <= parts.reorder_level:
			below_reorder += 1

		value = parts.stock_qty * parts.unit_cost
		total_value += value
			
		if parts.selling_price:
			margin = ((parts.selling_price - parts.unit_cost) / parts.selling_price) * 100
		else:
			margin = 0
		
		row["margin"] = round(margin,2)
		data.append(row)

		total_stock_qty += parts.stock_qty
	
	total_row = {
		"part_name": "TOTAL",
		"stock_qty": total_stock_qty,
		"unit_cost": "",
		"selling_price": total_value,
		"margin": ""
	}

	data.append(total_row)

	# report summary
	report_summary = [
		{
			"label": "Total Parts",
			"value": total_parts,
			"indicator": "blue"
		},
		{
			"label": "Below Reorder",
			"value": below_reorder,
			"indicator": "red"
		},
		{
			"label": "Total Inventory Value",
			"value": total_value,
			"indicator": "green"
		}
	]	

	return data, report_summary