import frappe
from frappe.desk.form.linked_with import get_linked_docs

@frappe.whitelist()
def get_si_link(docname):
	si = []
	linkinfo = {
		'Sales Invoice': {
			'child_doctype': 'Sales Invoice Item',
			'fieldname': ["sales_order"]
		}
	}
	docs = get_linked_docs('Sales Order', docname, linkinfo)
	
	for i in docs['Sales Invoice']:
		si.append(i.name)

	return si