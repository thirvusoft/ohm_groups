import frappe

def item_template(doc, actions):
    frappe.db.set_value("Item",doc.item_name,"quality_inspection_template",doc.name)
