import frappe

def warehouse_creation_from_branch(doc,actions):
    company = frappe.db.get_single_value("Global Defaults","default_company")
    abbr = frappe.db.get_value("Company",company,"abbr")
    if not frappe.db.exists("Warehouse", {'parent_warehouse': f'Supplier Warehouse - {abbr}', 'warehouse_name':doc.branch}):
        document=frappe.new_doc("Warehouse")
        document = frappe.new_doc("Warehouse")
        document.parent_warehouse =f'Supplier Warehouse - {abbr}'
        document.company = company
        document.warehouse_name = doc.branch
        document.flags.ignore_mandatory=True
        document.insert(ignore_permissions=True)
        doc.warehouse=document.name
        doc.save()