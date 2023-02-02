# Copyright (c) 2022, thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document




@frappe.whitelist()
def get_items(party_type = None, party = None):
	items_dc = []
	items_po = []
	if not party:
		return f"<p>Kindly Select the Goods Received From and Party</p>","Error Message"
	
	if party_type == "DC Not for Sales":
		dc_items = frappe.get_doc(party_type,party)
		for i in dc_items.items:
			items_dc.append({"item_code":i.item_code,"item_name":i.item_name,"qty":i.balance_qty})
		if dc_items.docstatus == 0:
				return f"<p>{party} Document is Not Submitted. Kindly Submit</p>","Error Message"
	else:
		po_items = frappe.get_doc(party_type,party)
		for i in po_items.items:
			items_po.append({"item_code":i.item_code,"item_name":i.item_name,"qty":i.qty})
		if po_items.docstatus == 0:
			return f"<p>{party} Document is Not Submitted. Kindly Submit</p>","Error Message"
	return items_dc,items_po
		
    
class GateEntry(Document):
    def on_submit(self):
        if self.party_type == "DC Not for Sales":
            for i in self.items:
                frappe.db.set_value('DC Items', {'parent': self.party,'parenttype':self.party_type,'item_code':i.item_code}, 'received_qty',i.received_qty)
                frappe.db.set_value('DC Items', {'parent': self.party,'parenttype':self.party_type,'item_code':i.item_code}, 'balance_qty',i.balanced_qty)
                if i.balanced_qty == 0:
                    frappe.db.set_value("DC Items", {"parent": self.party,'parenttype':self.party_type,"item_code":i.item_code},"total",1)

    
    def on_cancel(self):
    	if self.party_type == "DC Not for Sales":
         for i in self.items:
            rec_qty = frappe.get_value("DC Items", {'parent': self.party,'parenttype':self.party_type,'item_code':i.item_code},'received_qty')
            frappe.db.set_value('DC Items', {'parent':  self.party,'parenttype':self.party_type, 'item_code':i.item_code}, 'received_qty',float(rec_qty) - i.received_qty)
            frappe.db.set_value('DC Items', {'parent':  self.party,'parenttype':self.party_type,'item_code':i.item_code}, 'balance_qty',i.balanced_qty + i.received_qty)
            frappe.db.set_value("DC Items", {"parent": self.party,'parenttype':self.party_type,"item_code":i.item_code},"total",0)