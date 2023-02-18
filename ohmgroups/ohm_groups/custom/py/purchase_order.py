import json
from erpnext.controllers.subcontracting_controller import make_rm_stock_entry
import frappe
from erpnext.buying.doctype.purchase_order.purchase_order import make_subcontracting_order
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
        items = frappe.db.get_value('UOM Conversion Detail',{'parent':items,'uom':'Kg'},'conversion_factor')
        return items

@frappe.whitelist()
def item_supplier(supplier_name):
    supplier_item = frappe.get_doc("Supplier",supplier_name)
    if(supplier_item.default_item ==1):
        supplier = frappe.get_all("Supplier wise item",{'parent':supplier_item.name,},pluck="item_code")
        return supplier

# @frappe.whitelist()
# def po_order(doc,actions):
#     a=make_subcontracting_order(doc.name)
#     a.save()
#     a.submit()