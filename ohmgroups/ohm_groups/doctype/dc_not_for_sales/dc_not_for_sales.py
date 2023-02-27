# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def on_insert(party):
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
def address_company(company):
    com_add = frappe.get_value("Dynamic Link", {"parenttype":"Address","link_doctype":"Company","link_name":company},"parent")
    com_plant_add = frappe.get_value('Address',{'name':com_add})
    return com_plant_add


@frappe.whitelist()
def branch_address_company(company, branch):
        # com_add = frappe.get_value("Dynamic Link", {"parenttype":"Address","link_doctype":"Company","link_name":company},"parent")
        branch_add = frappe.get_value("Branch",{"company":company,"branch":branch},"address")
        return branch_add
    
    
@frappe.whitelist()
def address_shipping(party_type, party):
    com_add = frappe.get_all("Dynamic Link", {"parenttype":"Address","link_doctype":party_type,"link_name":party},pluck="parent")
    for i in com_add:
        ship_add =  frappe.get_value('Address',{'address_type':'Shipping','name':i},"name")
        if ship_add:
            return ship_add
@frappe.whitelist()
def address_billing(party_type, party):
    com_add = frappe.get_all("Dynamic Link", {"parenttype":"Address","link_doctype":party_type,"link_name":party},pluck="parent")
    for i in com_add:
        bill_add =  frappe.get_value('Address',{'address_type':'Billing','name':i},"name")
        if bill_add:
            return bill_add

@frappe.whitelist()
def item_supplier(party):
    supplier_item = frappe.get_doc("Supplier",party)
    if(supplier_item.default_item ==1):
        supplier = frappe.get_all("Supplier wise item",{'parent':supplier_item.name,},pluck="item_code")
        return supplier

@frappe.whitelist()
def item_customer(party):
    customer_item = frappe.get_doc("Customer",party)
    if(customer_item._default_item ==1):
        customer = frappe.get_all("Customer Default Items",{'parent':customer_item.name,},pluck="item_code")
        return customer

class DCNotforSales(Document):

	
	def on_submit(self):
			company = frappe.db.get_single_value("Global Defaults","default_company")
			abbr = frappe.db.get_value("Company",company,"abbr")
			document = frappe.new_doc("Stock Entry")
			document.stock_entry_type ="Send to Subcontractor"
			document.from_warehouse =f"Stores - {abbr}"
			document.to_warehouse = self.warehouse
			document.dc_no = self.name,
			for i in self.items:
				document.append('items', dict(
				item_code = i.item_code,
				qty=i.qty,
				basic_rate=1,
				uom=i.uom,
				))
			document.save(ignore_permissions=True)
			document.submit()

	def on_cancel(self):
		if frappe.db.exists("Stock Entry",{"dc_no":self.name}):
			frappe.get_doc("Stock Entry",{"dc_no":self.name}).cancel()
		
	def on_trash(self):
		if frappe.db.exists("Stock Entry",{"dc_no":self.name}):
			frappe.get_doc("Stock Entry",{"dc_no":self.name}).delete()

	def validate(self):
		total_qty = 0
		for i in self.items:
			total_qty += i.qty 
		self.total_qty = total_qty
  
	