import frappe

def attribute_item(doc,actions):
    if(doc.name == "process"):
        for i in doc.item_attribute_values:
            if not frappe.db.exists("Item", {'item_name': i.attribute_value}):
                document = frappe.new_doc("Item")
                document.item_name =i.attribute_value
                document.item_code =i.attribute_value
                document.item_group = "Services"
                document.stock_uom = "Kg"
                document.save(ignore_permissions=True)

@frappe.whitelist()
def delete_item(item_name):
    frappe.delete_doc_if_exists("Item", item_name)
    