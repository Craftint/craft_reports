// Copyright (c) 2016, Dany and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Collection"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.get_today(), -1),
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
			"fieldname":"document",
			"label": __("Document"),
			"fieldtype": "Select",
			"options": ["Quotation", "Sales Invoice", "Sales Order"],
			"default":"Quotation"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"docstatus",
			"label":__("Document Status"),
			"fieldtype":"Select",
			"options":["Draft", "Submitted", "Cancelled"],
			"default":"Submitted"
		}
	]
};
