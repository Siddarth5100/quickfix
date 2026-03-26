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
			'fieldname': 'technician',
			'label': 'Technician',
			'fieldtype': 'Link',
			'options': 'Technician'
		},
		{
			'fieldname': 'total_jobs',
			'label': 'Total Jobs',
			'fieldtype': 'Data'
		},
		{
			'fieldname': 'completed',
			'label': 'Completed',
			'fieldtype': 'Data'
		},
		{
			'fieldname': 'avg_turnaround_days',
			'label': 'Avg Turnaround Days',
			'fieldtype': 'Int'
		},
		{
			'fieldname': 'revenue',
			'label': 'Revenue',
			'fieldtype': 'Int'
		},
		{
			'fieldname': 'completion_rate',
			'label': 'Completion Rate',
			'fieldtype': 'Int'
		}
	]

	device_type = frappe.get_all('Device Type', 'device_type')
	# print("----------------", device_type)

	for dt in device_type:
		# print("-----------", dt)
		columns.append({
			"label": dt['device_type'],
			"fieldname": dt['device_type'].lower().replace(" ", "_"),
			"fieldtype": "Int"
		})
	# print("------------------columns", columns)
	return columns

def get_data(filters):

	data = []
	# print("------UI----",filters.get("technician"))
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	technician = filters.get("technician")

	# print("-------testing ui---", from_date) eg: 2026-03-01
	# print("-----------test to date", to_date) eg: 2026-03-13
	# print("------UI----", technician) eg: TECH-0009

	# if technician name is available in UI
	if technician is not None:
		
		for tech in get_technician_name():
			if tech == technician:
				# print("Matched", tech, filters.get('technician'))
				# print("---tech", type(tech), "-----technician", type(technician))
				job_cards = frappe.get_list(
					'Job Card', 
					fields=["assigned_technician", "diagnosis_date"])

				total_jobs = 0
		
				for job in job_cards:
					if job["assigned_technician"] == tech:
						# if from_date <= job["diagnosis_date"]:
							total_jobs += 1

				row = {
					"technician": tech,
					"total_jobs": total_jobs
				}
				
				data.append(row)
			
				
	# if not show all technicians
	else:
		for tech in get_technician_name():
			# data-------- TECH-0009 <class 'str'>
			# print("data--------", tech, type(tech))
			row = {
				"technician": tech
			}

			data.append(row)

	return data
	

# technician name from jobcard
def get_technician_name():

	# emplty list to store
	all_techs = []
	
	# frappe orm to get name(technician_name) from job card as list
	technician = frappe.get_all('Technician', 'name')
	for tech in technician:
		all_techs.append(tech['name'])

	# print(all_techs, "names" , type(all_techs))
	# eg: ['TECH-0003'] names <class 'list'>
	return all_techs

	#  eg: data-------- TECH-0009 <class 'str'


