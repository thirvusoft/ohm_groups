from erpnext.buying.doctype.purchase_order.purchase_order import set_missing_values
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate


@frappe.whitelist()
def material_request_item(source_name, target_doc=None):
	def update_item(obj, target, source_parent):
		target.qty = flt(obj.qty) - flt(obj.received_qty)
		target.stock_qty = (flt(obj.qty) - flt(obj.received_qty))
		target.amount = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
		target.base_amount = (
			(flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
		)

	doc = get_mapped_doc(
		"Material Request",
		source_name,
		{
			"Material Request": {
				"doctype": "Purchase Receipt",
				"field_map": {"supplier_warehouse": "supplier_warehouse"},
				"validation": {
					"docstatus": ["=", 1],
				},
			},
   
			"Material Request Item": {
				"doctype": "Purchase Receipt Item",
				"field_map": {
					"name": "material_request_item",
					"parent": "material_request",
					"bom": "bom",
					"material_request": "material_request",
					"material_request_item": "material_request_item",
				},
				"postprocess": update_item,
				"condition": lambda doc: abs(doc.received_qty) < abs(doc.qty)
			},
			"Purchase Taxes and Charges": {"doctype": "Purchase Taxes and Charges", "add_if_empty": True},
		},
		target_doc,
		set_missing_values,
	)
	doc.set_onload("ignore_price_list", True)

	return doc

def update_item_(doc, actions):
	for i in doc.items:
		if i.material_request:
			ordered_qty = frappe.get_value("Material Request Item", {'parent':i.material_request,'item_code':i.item_code},'ordered_qty')
			frappe.db.set_value('Material Request Item', {'parent': i.material_request, 'item_code':i.item_code}, 'ordered_qty', i.qty + ordered_qty )
			frappe.db.set_value('Material Request', i.material_request, 'per_ordered', 100 )
		
	# Stock Entry Created -> Material Transfer
	# if doc.is_gate_entry:
	# 	company = frappe.db.get_single_value("Global Defaults","default_company")
	# 	abbr = frappe.db.get_value("Company",company,"abbr")
	# 	document = frappe.new_doc("Stock Entry")
	# 	document.stock_entry_type ="Material Transfer"
	# 	for i in doc.items:
	# 		item = frappe.get_doc("Item",{"name":i.item_code})
	# 		for j in item.uoms:
	# 			if item.stock_uom == j.uom:
	# 				document.append('items', dict(
	# 					item_code = i.item_code,
	# 					item_name = i.item_name,
	# 					s_warehouse = i.warehouse,
	# 					t_warehouse = f'Stores - {abbr}',
	# 					qty=i.qty,
	# 					basic_rate=1,
	# 					stock_uom = item.stock_uom,
	# 					uom=i.uom,
	# 					reference_purchase_receipt = doc.name
	# 				))
	# 	document.save(ignore_permissions=True)
	# 	document.submit()
	
def cancel_item_(doc, actions):
	for i in doc.items:
		if i.material_request:
			ordered_qty = frappe.get_value("Material Request Item", {'parent':i.material_request,'item_code':i.item_code},'ordered_qty')
			received_per = frappe.get_value("Material Request", i.material_request,'per_received')
			if received_per == 0:
					frappe.db.set_value('Material Request', i.material_request, 'per_ordered', 0 )
			frappe.db.set_value('Material Request Item', {'parent': i.material_request, 'item_code':i.item_code}, 'ordered_qty', ordered_qty - i.qty)
   
def check_qc(doc,actions):
	qc = frappe.get_all("Quality Inspection", filters={'reference_type': "Purchase Receipt", 'reference_name': doc.name})
	if not qc:
		frappe.throw("Kindly check the quality Inspection")
	url = frappe.utils.get_url()
	for i in qc:
		qi_doc = frappe.get_doc("Quality Inspection", i.name)
		if qi_doc.docstatus != 1:
			frappe.throw(f'Kindly submit the <a href="{url}/app/quality-inspection/{qi_doc.name}">{qi_doc.doctype}</a> document')

