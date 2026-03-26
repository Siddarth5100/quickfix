// Copyright (c) 2026, Siddarth and contributors
// For license information, please see license.txt

frappe.query_reports["Spare Parts Inventory"] = {

	formatter: function (value, row, column, data, default_formatter) {

    value = default_formatter(value, row, column, data);

	if (data.stock_qty <= data.reorder_level) {
    value = `<div style="background-color:#ffcccc">${value}</div>`;
	}

    return value;
	}
};
