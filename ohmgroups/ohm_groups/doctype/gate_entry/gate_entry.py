# Copyright (c) 2022, thirvusoft and contributors
# For license information, please see license.txt

import json
from erpnext.buying.doctype.purchase_order.purchase_order import set_missing_values
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate
from frappe.model.document import Document




@frappe.whitelist()
def get_items(party_type = None, purchase_order = None, dc_not_for_sales = None):
    items_dc = []
    items_po = []
    
    
    if not party_type:
        return f"<p>Kindly Select the Goods Received From and Party</p>","Error Message"

    if party_type == "DC Not for Sales":
        dc = json.loads(dc_not_for_sales)
        for m in dc:
            dc_items = frappe.get_doc(party_type,{"name":m.get('goods_received_from')})
            if dc_items.docstatus == 0:
                return f"<p>{m.get('goods_received_from')} Document is Not Submitted. Kindly Submit</p>","Error Message"
            if dc_items.docstatus == 2:
                return f"<p>{m.get('goods_received_from')} Cancelled Document is Not Allowed</p>","Error Message"	
            
            for i in dc_items.items:
                if dc_items.docstatus == 1:
                    items_dc.append({"item_code":i.item_code,"item_name":i.item_name,"qty":flt(i.balance_qty),"uom":i.uom,"document_no":m.get('goods_received_from'),"name1":dc_items.party})
        return items_dc
    elif party_type == "Purchase Order":
        po = json.loads(purchase_order)
        for n in po:
            po_items = frappe.get_doc(party_type,{"name":n.get('goods_received_from')})
            if po_items.docstatus == 0:
                return f"<p>{n.get('goods_received_from')} Document is Not Submitted. Kindly Submit</p>","Error Message"
            if po_items.docstatus == 2:
                    return f"<p>{n.get('goods_received_from')} Cancelled Document is Not Allowed</p>","Error Message"
            for i in po_items.items:
                if po_items.docstatus == 1 and i.qty - i.received_qty > 0:
                    items_po.append({"item_code":i.item_code,"item_name":i.item_name,"qty": i.qty - i.received_qty,"uom":i.uom,"document_no":n.get('goods_received_from'),"name1":po_items.naming_supplier})
        return items_po

@frappe.whitelist()
def gate_entry_item(source_name, target_doc=None):
    def update_item(obj, target, source_parent):
        frappe.errprint(target,obj)
        target.qty = flt(obj.qty) - flt(obj.received_qty)
        target.stock_qty = (flt(obj.qty) - flt(obj.received_qty))
        target.amount = (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
        target.base_amount = (
            (flt(obj.qty) - flt(obj.received_qty)) * flt(obj.rate)
        )

    doc = get_mapped_doc(
        "Gate Entry",
        source_name,
        {
            "Gate Entry": {
                "doctype": "Purchase Receipt",
                "field_map": {"supplier_warehouse": "supplier_warehouse"},
                "validation": {
                    "docstatus": ["=", 1],
                },
            },
   
            "Material Request Item": {
                "doctype": "Purchase Receipt Item",
                "field_map": {
                    "name": "gate_entry_item",
                    "parent": "gate_entry",
                    "bom": "bom",
                    "gate_entry": "gate_entry",
                    "gate_entry_item": "gate_entry_item",
                },
                "postprocess": update_item,
                "condition": lambda doc: abs(doc.received_qty) < abs(doc.qty)
            },
            "Purchase Taxes and Charges": {"doctype": "Purchase Taxes and Charges", "add_if_empty": True},
        },
        target_doc,
        set_missing_values,
    )
    doc.set_onload("ignore_price_list", True)

    return doc
            
    
class GateEntry(Document):
    def on_submit(self):
        if self.party_type == "DC Not for Sales":

                for i in self.items:
                    frappe.db.set_value('DC Items', {
                                        'parent': i.document_no,
                                        'parenttype': self.party_type,
                                        'item_code': i.item_code
                                        }, 'received_qty', i.received_qty)
                    frappe.db.set_value('DC Items', {
                                        'parent': i.document_no,
                                        'parenttype': self.party_type,
                                        'item_code': i.item_code
                                        }, 'balance_qty', i.balanced_qty)
                    if i.balanced_qty == 0:
                        frappe.db.set_value("DC Items", {
                            'parent': i.document_no,
                            'parenttype': self.party_type,
                            'item_code': i.item_code
                            }, "total", 1)
        elif self.party_type == "Purchase Order":
                for i in self.items:
                    rec_qty = frappe.get_value("Purchase Order Item", {'parent': i.document_no,'parenttype':self.party_type,'item_code':i.item_code},'received_qty') or 0
                    frappe.db.set_value('Purchase Order Item', {'parent': i.document_no,'parenttype':self.party_type,'item_code':i.item_code}, 'received_qty',rec_qty + i.received_qty)
                document = frappe.new_doc("Stock Entry")
                document.stock_entry_type ="Material Receipt"
                document.to_warehouse = self.warehouse
                for i in self.items:
                    item = frappe.get_doc("Item",{"name":i.item_code})
                    for j in item.uoms:
                        if item.stock_uom == j.uom:
                            document.append('items', dict(
                                item_code = i.item_code,
                                qty=i.received_qty,
                                basic_rate=1,
                                stock_uom = item.stock_uom,
                                uom=i.uom,
                                transfer_qty=i.received_qty,
                                conversion_factor = j.conversion_factor
                            ))
                document.save(ignore_permissions=True)
                document.submit()
                if self.party_type == "Purchase Order":
                    document = frappe.new_doc("Purchase Receipt")
                    document.is_gate_entry = 1
                    for i in self.items:
                        
                        document.supplier =i.name1
                        item = frappe.get_doc("Item",{"name":i.item_code})
                        document.append('items', dict(
                            item_code = i.item_code,
                            item_name = i.item_name,
                            
                            qty=i.received_qty,
                            uom=i.uom,
                            warehouse=self.warehouse,
                            purchase_order = i.document_no
                        ))
                    document.save(ignore_permissions=True)
                elif self.party_type == "Supplier":
                    document = frappe.new_doc("Purchase Receipt")
                    document.is_gate_entry = 1
                    for i in self.items:
                        
                        document.supplier =i.name1
                        item = frappe.get_doc("Item",{"name":i.item_code})
                        document.append('items', dict(
                            item_code = i.item_code,
                            item_name = i.item_name,
                            qty=i.received_qty,
                            uom=i.uom,
                            warehouse=self.warehouse,
                        ))
                    document.save(ignore_permissions=True)


    
    def on_cancel(self):
        if self.party_type == "DC Not for Sales":
            for i in self.items:
                rec_qty = frappe.get_value("DC Items", {'parent': i.document_no,'parenttype':self.party_type,'item_code':i.item_code},'received_qty')
                frappe.db.set_value('DC Items', {'parent':  i.document_no,'parenttype':self.party_type, 'item_code':i.item_code}, 'received_qty',float(rec_qty) - i.received_qty)
                frappe.db.set_value('DC Items', {'parent':  i.document_no,'parenttype':self.party_type,'item_code':i.item_code}, 'balance_qty',i.balanced_qty + i.received_qty)
                frappe.db.set_value("DC Items", {"parent": i.document_no,'parenttype':self.party_type,"item_code":i.item_code},"total",0)
        if self.party_type == "Purchase Order":
             for i in self.items:
                rec_qty = frappe.get_value("Purchase Order Item", {'parent': i.document_no,'parenttype':self.party_type,'item_code':i.item_code},'received_qty') or 0
                frappe.db.set_value('Purchase Order Item', {'parent':  i.document_no,'parenttype':self.party_type, 'item_code':i.item_code}, 'received_qty',rec_qty - i.received_qty)
        if frappe.db.exists("Stock Entry",{"dc_no":self.name}):
            frappe.get_doc("Stock Entry",{"dc_no":self.name}).cancel()
   
    def on_trash(self):
        if frappe.db.exists("Stock Entry",{"dc_no":self.name}):
            frappe.get_doc("Stock Entry",{"dc_no":self.name}).delete()
         