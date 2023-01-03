# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

@frappe.whitelist()
def on_insert(party):
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

class DCNotforSales(Document):

	
	def on_submit(self):
			document = frappe.new_doc("Stock Entry")
			document.stock_entry_type ="Send to Subcontractor"
			document.from_warehouse ="Stores - ONE"
			document.to_warehouse = self.warehouse
			document.dc_no = self.name,
			for i in self.items:
				document.append('items', dict(
				item_code = i.item_code,
				qty=i.qty,
				basic_rate=i.rate,
				uom=i.uom,
				))
			document.save(ignore_permissions=True)
			document.submit()

	def on_cancel(self):
		frappe.get_doc("Stock Entry",{"dc_no":self.name}).cancel()
		
	def on_trash(self):
		frappe.get_doc("Stock Entry",{"dc_no":self.name}).delete()