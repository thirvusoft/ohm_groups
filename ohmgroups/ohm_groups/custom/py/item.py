import frappe

def item_variant(doc,actions):
    if doc.is_group == 1:
        doc.parent_item = doc.variant_of

def get_item_defaults_(item_code):
	item = frappe.get_cached_doc("Item", item_code)
	m = []
	for d in item.supplier_items:
		m.append(d.supplier) 
	return m
