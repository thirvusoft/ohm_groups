import frappe

def check_qc(doc,actions):
	qc = frappe.get_all("Quality Inspection", filters={'reference_type': "Purchase Invoice", 'reference_name': doc.name})
	if not qc:
		frappe.throw("Kindly check the quality Inspection")
	url = frappe.utils.get_url()
	for i in qc:
		qi_doc = frappe.get_doc("Quality Inspection", i.name)
		if qi_doc.docstatus != 1:
			frappe.throw(f'Kindly submit the <a href="{url}/app/quality-inspection/{qi_doc.name}">{qi_doc.doctype}</a> document')