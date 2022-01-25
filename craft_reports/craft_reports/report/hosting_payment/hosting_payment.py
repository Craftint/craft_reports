# Copyright (c) 2013, Dany and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
import frappe
from frappe.utils import flt
import datetime

def execute(filters=None):
	data = []
	columns = [
		_("Customer") + ":Link/Customer:250", _("Detail") + "::150",
		_("Payment Date") + ":Date:120", _("Paid Amount") + ":Currency:200",
		_("Unpaid Amount") + ":Currency:200"
	]

	filter_start = datetime.datetime.strptime(filters.get("from_date"), '%Y-%m-%d').date()
	filter_end = datetime.datetime.strptime(filters.get("to_date"), '%Y-%m-%d').date()
	cust = filters.get("customer")
	status = filters.get("docstatus")
	condition = ''

	if cust:
		condition += """ and customer = '{0}'""".format(cust)

	if status:
		condition += """ and status = '{0}'""".format(status)

	documents = frappe.db.sql("""SELECT customer FROM `tabHosting Details` WHERE payment_by = 'Craft Interactive'{0}""".format(condition), as_dict=1)

	for doc in documents:
		payment = frappe.db.sql("""
		SELECT item_code, scheduled_date, amount, paid
		FROM `tabHosting Payments`
		WHERE parent = '{0}' AND scheduled_date >= '{1}' AND scheduled_date <= '{2}'""".format(doc.customer, filter_start, filter_end), as_dict=1)

		for d in payment:
			paid_amt = 0.00
			unpaid_amt = flt(d.amount)
			if d.paid:
				paid_amt = flt(d.amount)
				unpaid_amt = 0.00

			row = [doc.customer, d.item_code, d.scheduled_date, paid_amt, unpaid_amt]
			data.append(row)

		amc = frappe.db.sql("""
		SELECT item_code, scheduled_date, amount, received
		FROM `tabHosting Schedule`
		WHERE parent = '{0}' AND scheduled_date >= '{1}' AND scheduled_date <= '{2}'""".format(doc.customer, filter_start, filter_end), as_dict=1)

		for d in amc:
			paid_amt = 0.00
			unpaid_amt = flt(d.amount)
			if d.received:
				paid_amt = flt(d.amount)
				unpaid_amt = 0.00

			row = [doc.customer, d.item_code, d.scheduled_date, paid_amt, unpaid_amt]
			data.append(row)

	return columns, data