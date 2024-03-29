from erpnext.stock.doctype.material_request.material_request import set_missing_values, update_item
import frappe
import json
from erpnext.stock.doctype.item.item import get_item_defaults
from ohmgroups.ohm_groups.custom.py.item import get_item_defaults_
from frappe.model.mapper import get_mapped_doc
from frappe.utils.data import flt, getdate, nowdate

@frappe.whitelist()
def make_purchase_receipt(source_name, target_doc=None, args=None):
	if args is None:
		args = {}
	if isinstance(args, str):
		args = json.loads(args)

	def postprocess(source, target_doc):
		if frappe.flags.args and frappe.flags.args.default_supplier:
			# items only for given default supplier
			supplier_items = []
			for d in target_doc.items:
				default_supplier = get_item_defaults(d.item_code, target_doc.company).get("default_supplier")
				if frappe.flags.args.default_supplier == default_supplier:
					supplier_items.append(d)
			target_doc.items = supplier_items

		set_missing_values(source, target_doc)

	def select_item(d):
		filtered_items = args.get("filtered_children", [])
		child_filter = d.name in filtered_items if filtered_items else True

		return d.ordered_qty < d.stock_qty and child_filter

	doclist = get_mapped_doc(
		"Material Request",
		source_name,
		{
			"Material Request": {
				"doctype": "Purchase Receipt",
				"validation": {"docstatus": ["=", 1], "material_request_type": ["=", "Purchase"]},
			},
			"Material Request Item": {
				"doctype": "Purchase Receipt Item",
				"field_map": [
					["name", "material_request_item"],
					["parent", "material_request"],
					["uom", "stock_uom"],
					["uom", "uom"],
					["sales_order", "sales_order"],
					["sales_order_item", "sales_order_item"],
				],
				"postprocess": update_item,
				"condition": select_item,
			},
		},
		target_doc,
		postprocess,
	)

	return doclist
@frappe.whitelist()
def item_supplier(supplier):
    supplier_item = frappe.get_doc("Supplier",supplier)
    if(supplier_item.default_item ==1):
        supplier = frappe.get_all("Supplier wise item",{'parent':supplier_item.name,},pluck="item_code")
        return supplier


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_default_supplier_query(doctype, txt, searchfield, start, page_len, filters):
	doc = frappe.get_doc("Material Request", filters.get("doc"))
	item_list = []
	for d in doc.items:
		if(d.ordered_qty != d.qty):
			item_list.append(d.item_code)

	return frappe.db.sql(
		"""select supplier
		from `tabItem Supplier`
		where parent in ({0}) and
		supplier IS NOT NULL
		""".format(
			", ".join(["%s"] * len(item_list))
		),
		tuple(item_list),
	)

@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None, args=None):
	if args is None:
		args = {}
		
	if isinstance(args, str):
		args = json.loads(args)

	def postprocess(source, target_doc):
		
		if frappe.flags.args and frappe.flags.args.default_supplier:
	
			# items only for given default supplier
			supplier_items = []
			for d in target_doc.items:

				default_supplier = get_item_defaults_(d.item_code)
				for i in default_supplier:
					if frappe.flags.args.default_supplier == i:
					
						supplier_items.append(d)
			target_doc.items = supplier_items

		set_missing_values(source, target_doc)

	def select_item(d):
		filtered_items = args.get("filtered_children", [])
		child_filter = d.name in filtered_items if filtered_items else True

		return d.ordered_qty < d.stock_qty and child_filter

	doclist = get_mapped_doc(
		"Material Request",
		source_name,
		
		{
			"Material Request": {
				"doctype": "Purchase Order",
				"validation": {"docstatus": ["=", 1], "material_request_type": ["=", "Purchase"]},
				"field_map" :[
					["default_supplier", "naming_supplier"]
				]
			},
			"Material Request Item": {
				"doctype": "Purchase Order Item",
				"field_map": [
					["name", "material_request_item"],
					["parent", "material_request"],
					["uom", "stock_uom"],
					["uom", "uom"],
					["sales_order", "sales_order"],
					["sales_order_item", "sales_order_item"],
				],
				"postprocess": update_item,
				"condition": select_item,
			},
		},
		target_doc,
		postprocess,
	)
	doclist.update({
		"naming_supplier" : frappe.flags.args.default_supplier
	})
	return doclist