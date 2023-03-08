import json
from erpnext.controllers.subcontracting_controller import make_rm_stock_entry
import frappe
from erpnext.buying.doctype.purchase_order.purchase_order import make_subcontracting_order
from frappe.utils.data import flt
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

def submit(doc,actions):
        for i in doc.items:
            if i.material_request:
                rec_qty = (frappe.get_value("Material Request Item", {'parent': i.material_request,'item_code':i.item_code},'pending_qty') or 0)
                frappe.db.set_value('Material Request Item', {'parent': i.material_request, 'item_code':i.item_code}, 'pending_qty', flt(rec_qty) -i.qty )

def cancel(doc,actions):
        for i in doc.items:
            if i.material_request:
                rec_qty = (frappe.get_value("Material Request Item", {'parent': i.material_request,'item_code':i.item_code},'pending_qty') or 0)
                frappe.db.set_value('Material Request Item', {'parent': i.material_request, 'item_code':i.item_code}, 'pending_qty',flt(rec_qty) + i.qty)