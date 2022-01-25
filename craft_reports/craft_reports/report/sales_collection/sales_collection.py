# Copyright (c) 2013, Dany and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _
import datetime
import calendar

def execute(filters=None):
	if not filters:
		return [], []
	data = []
	columns = [
		_("Client") + ":Link/Customer:350",
		_("Voucher No") + ":Dynamic Link/" + filters.get("document") + ":140",
		_("Lead Owner") + ":Link/User:170", _("Sales Person") + ":Link/Employee:170",
		_("Amount") + ":Currency:150", _("Status") + "::120"
	]

	lead_owner = get_lead_owner()
	sales_person = get_sales_person()

	if filters.get("document") == "Quotation":
		dispdata = get_quotations(filters)

	if filters.get("document") == "Sales Invoice":
		dispdata = get_sales_invoice(filters)

	if filters.get("document") == "Sales Order":
		dispdata = get_sales_order(filters)

	if dispdata:
		for i in dispdata:
			data.append([i.customer_name, i.name, lead_owner.get(i.party_name), sales_person.get(i.party_name), i.base_grand_total, i.status])

	return columns, data

def get_lead_owner():
	return	frappe._dict(frappe.db.sql("""
				SELECT
					name,
					lead_owner
				FROM `tabLead`
				"""))

def get_sales_person():
	return	frappe._dict(frappe.db.sql("""
				SELECT
					name,
					sales_person
				FROM `tabLead`
				"""))

def get_quotations(filters):
	filters.update({"from_date": filters.get("from_date"), "to_date":filters.get("to_date")})
	#frappe.throw(str(filters))
	conditions, filters = get_conditions(filters)
	quo = frappe.db.sql("""
		select name, customer_name, base_grand_total, status, party_name
		from `tabQuotation` 
		where %s
		order by name""" % conditions, filters, as_dict=1)

	return quo or []

def get_sales_order(filters):
	filters.update({"from_date": filters.get("from_date"), "to_date":filters.get("to_date")})
	#frappe.throw(str(filters))
	conditions, filters = get_conditions(filters)
	so = frappe.db.sql("""
		select name, customer_name, base_grand_total, status
		from `tabSales Order` 
		where %s
		order by name""" % conditions, filters, as_dict=1)

	return so or []

def get_sales_invoice(filters):
	filters.update({"from_date": filters.get("from_date"), "to_date":filters.get("to_date")})
	#frappe.throw(str(filters))
	conditions, filters = get_si_conditions(filters)
	si = frappe.db.sql("""
		select name, customer_name, base_grand_total, status
		from `tabSales Invoice` 
		where %s
		order by name""" % conditions, filters, as_dict=1)

	return si or []

def get_conditions(filters):
	conditions = ""
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

	if filters.get("docstatus"):
		conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])

	if filters.get("from_date"): conditions += " and transaction_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and transaction_date <= %(to_date)s"
	if filters.get("company"): conditions += " and company = %(company)s"

	return conditions, filters

def get_si_conditions(filters):
	conditions = ""
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

	if filters.get("docstatus"):
		conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])

	if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date <= %(to_date)s"
	if filters.get("company"): conditions += " and company = %(company)s"

	return conditions, filters