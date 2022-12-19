import json
import frappe

@frappe.whitelist()
def on_insert(supplier,is_subcontracted):
    if is_subcontracted:
        company = frappe.db.get_single_value("Global Defaults","default_company")
        abbr = frappe.db.get_value("Company",company,"abbr")
        if not frappe.db.exists("Warehouse", {'parent_warehouse': f'Supplier Warehouse - {abbr}', 'warehouse_name':supplier}):
            document = frappe.new_doc("Warehouse")
            document.parent_warehouse =f'Supplier Warehouse - {abbr}'
            document.company = company
            document.warehouse_name = supplier
            document.save(ignore_permissions=True)
            return document.name
        else:
            return frappe.get_value("Warehouse", {'parent_warehouse': f'Supplier Warehouse - {abbr}', 'warehouse_name':supplier}, pluck="name")

@frappe.whitelist()        
def uom_qty(items, is_subcontracted):
    if is_subcontracted:
        items = json.loads(items)
        for i in items:
            items = frappe.db.get_value("UOM Conversion Detail",{'parent':i['fg_item'],'uom':"Kg"},"conversion_factor")
            return items

@frappe.whitelist()
def item_supplier(supplier):
    supplier_item = frappe.get_doc("Supplier",supplier)
    if(supplier_item.default_item ==1):
        supplier = frappe.get_all("Supplier wise item",{'parent':supplier_item.name,},pluck="item_code")
        return supplier