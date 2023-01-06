# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def grn_on_insert(party):
    if party:
        company = frappe.db.get_single_value("Global Defaults","default_company")
        abbr = frappe.db.get_value("Company",company,"abbr")
        if not frappe.db.exists("Warehouse", {'parent_warehouse': f'Supplier Warehouse - {abbr}', 'warehouse_name':party}):
            document = frappe.new_doc("Warehouse")
            document.parent_warehouse =f'Supplier Warehouse - {abbr}'
            document.company = company
            document.warehouse_name = party
            document.save(ignore_permissions=True)
            return document.name
        else:
            return frappe.get_value("Warehouse", {'parent_warehouse': f'Supplier Warehouse - {abbr}', 'warehouse_name':party}, pluck="name")
        
@frappe.whitelist()
def grn_address_company(company):
    com_add = frappe.get_value("Dynamic Link", {"parenttype":"Address","link_doctype":"Company","link_name":company},"parent")
    com_plant_add = frappe.get_value('Address',{'name':com_add})
    return com_plant_add


# @frappe.whitelist()
# def grn_branch_address_company(company):
#         # com_add = frappe.get_value("Dynamic Link", {"parenttype":"Address","link_doctype":"Company","link_name":company},"parent")
#         branch_add = frappe.get_value("Branch",{"company":company,"branch":branch},"address")
#         return branch_add
    
    
@frappe.whitelist()
def grn_address_shipping(party_type, party):
    com_add = frappe.get_all("Dynamic Link", {"parenttype":"Address","link_doctype":party_type,"link_name":party},pluck="parent")
    for i in com_add:
        ship_add =  frappe.get_value('Address',{'address_type':'Shipping','name':i},"name")
        if ship_add:
            return ship_add
@frappe.whitelist()
def grn_address_billing(party_type, party):
    com_add = frappe.get_all("Dynamic Link", {"parenttype":"Address","link_doctype":party_type,"link_name":party},pluck="parent")
    for i in com_add:
        bill_add =  frappe.get_value('Address',{'address_type':'Billing','name':i},"name")
        if bill_add:
            return bill_add        
        
@frappe.whitelist()
def grn_dc_items(items,company,party,party_type):
    get_dc_all = frappe.get_all("DC Not for Sales",{"company":company,"party":party,"party_type":party_type})
    dc_doc=[]
    for i in get_dc_all:
        get_dc_doc = frappe.get_doc("DC Not for Sales",{"name":i.name})
        for j in get_dc_doc.items:
            if j.item_code == items:
            # get_dc_items = frappe.get_all("DC Items",{"items":j.item_code,"parent":})
                dc_doc.append({"dc_no":get_dc_doc.name,"item_code":j.item_code,"qty":j.qty})
    return dc_doc
            
     
     
     
class GoodsReceivedNotes(Document):
	pass

