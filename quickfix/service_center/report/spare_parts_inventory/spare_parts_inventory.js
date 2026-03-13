// Copyright (c) 2026, Siddarth and contributors
// For license information, please see license.txt

frappe.query_reports["Spare Parts Inventory"] = {
	// "filters": [

	// ]

	formatter: function (value, row, column, data, default_formatter) {
		

    value = default_formatter(value, row, column, data);
	
    value = `<span style="background-color:red">${value}</span>`;

    return value;

	}
	
};
