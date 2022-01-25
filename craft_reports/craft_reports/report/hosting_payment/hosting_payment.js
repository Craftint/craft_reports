// Copyright (c) 2016, Dany and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Hosting Payment"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(),-1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"docstatus",
			"label":__("Status"),
			"fieldtype":"Select",
			"options":["Pending", "Active", "Ended"],
			"default":"Active"
		}
	]
};
