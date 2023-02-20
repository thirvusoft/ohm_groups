import frappe

def item_variant(doc,actions):
    if doc.variant_of:
        doc.parent_item = doc.variant_of