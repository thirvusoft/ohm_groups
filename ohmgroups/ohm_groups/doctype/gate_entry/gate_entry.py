# Copyright (c) 2022, thirvusoft and contributors
# For license information, please see license.txt

import json
from erpnext.buying.doctype.purchase_order.purchase_order import set_missing_values
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate
from frappe.model.document import Document
from ohmgroups.ohm_groups.doctype.grn.grn import grn_on_insert
from ohmgroups.ohm_groups.doctype.grn.grn import grn_address_billing
from ohmgroups.ohm_groups.doctype.grn.grn import grn_address_shipping
from frappe.model.naming import make_autoname

@frappe.whitelist()
def get_items(party_type = None, against_po__dc = None, purchase_order = None, dc_not_for_sales = None, party_name = None, is_gate_entry_in__out = None,against_si__dc = None,sales_invoice = None):
    items_dc = []
    items_po = []
    items_si = []
    
    if not is_gate_entry_in__out :
        return f"<p>Kindly Select the Entry Type </p>","Error Message"
    elif not party_type:
        return f"<p>Kindly Select the Party Type  </p>","Error Message"
    elif not party_name:
        return f"<p>Kindly Select the Party Name  </p>","Error Message"
    elif not against_po__dc and is_gate_entry_in__out == "IN":
        return f"<p>Kindly Select the Get Items From  </p>","Error Message"
    elif not against_si__dc and is_gate_entry_in__out == "OUT":
        return f"<p>Kindly Select the Get Items From  </p>","Error Message"
    elif not purchase_order and against_po__dc == "Purchase Order" :
        return f"<p>Kindly Select the Purchase Order </p>","Error Message"
    elif not dc_not_for_sales and against_po__dc == "DC Not for Sales" :
        return f"<p>Kindly Select the DC Not for Sales </p>","Error Message"
    elif not dc_not_for_sales and against_si__dc == "DC Not for Sales" :
        return f"<p>Kindly Select the DC Not for Sales </p>","Error Message"
    elif not sales_invoice and against_si__dc == "Sales Invoice":
        return f"<p>Kindly Select the Sales Invoice </p>","Error Message"

    if against_po__dc == "DC Not for Sales" or against_si__dc == "DC Not for Sales":
        dc = json.loads(dc_not_for_sales)
        for m in dc:
            dc_items = frappe.get_doc("DC Not for Sales",{"name":m.get('goods_received_from'),"party_type" : party_type, "party":party_name})
            if dc_items.docstatus == 0:
                return f"<p>{m.get('goods_received_from')} Document is Not Submitted. Kindly Submit</p>","Error Message"
            if dc_items.docstatus == 2:
                return f"<p>{m.get('goods_received_from')} Cancelled Document is Not Allowed</p>","Error Message"	
            
            for i in dc_items.items:
                if dc_items.docstatus == 1 and is_gate_entry_in__out == "IN" :
                    if flt(i.balance_qty) != 0:
                        items_dc.append({"description":i.description,"item_code":i.item_code,"item_name":i.item_name,"qty":flt(i.balance_qty),"uom":i.uom,"document_no":m.get('goods_received_from'),"name1":dc_items.party})
                else:
                    items_dc.append({"description":i.description,"item_code":i.item_code,"item_name":i.item_name,"qty":flt(i.qty),"uom":i.uom,"document_no":m.get('goods_received_from'),"name1":dc_items.party})
        return items_dc
    elif against_po__dc == "Purchase Order":
        po = json.loads(purchase_order)
        for n in po:
            po_items = frappe.get_doc(against_po__dc,{"name":n.get('goods_received_from')})
            if po_items.docstatus == 0:
                return f"<p>{n.get('goods_received_from')} Document is Not Submitted. Kindly Submit</p>","Error Message"
            if po_items.docstatus == 2:
                    return f"<p>{n.get('goods_received_from')} Cancelled Document is Not Allowed</p>","Error Message"
            for i in po_items.items:
                if po_items.docstatus == 1 and i.qty - i.received_qty > 0 :
                    items_po.append({"item_code":i.item_code,"item_name":i.item_name,"qty": i.qty - i.received_qty,"uom":i.uom,"document_no":n.get('goods_received_from'),"name1":po_items.naming_supplier})
        return items_po
    elif against_si__dc == "Sales Invoice":
        po = json.loads(sales_invoice)
        for n in po:
            po_items = frappe.get_doc(against_si__dc,{"name":n.get('goods_received_from')})
            if po_items.docstatus == 0:
                return f"<p>{n.get('goods_received_from')} Document is Not Submitted. Kindly Submit</p>","Error Message"
            if po_items.docstatus == 2:
                    return f"<p>{n.get('goods_received_from')} Cancelled Document is Not Allowed</p>","Error Message"
            for i in po_items.items:
                if po_items.docstatus == 1 :
                    items_si.append({"item_code":i.item_code,"item_name":i.item_name,"qty": i.qty ,"uom":i.uom,"document_no":n.get('goods_received_from'),"name1":po_items.customer})
        return items_si
          
@frappe.whitelist()
def item_supplier(party_name):
    supplier_item = frappe.get_doc("Supplier",party_name)
    if(supplier_item.default_item ==1):
        supplier = frappe.get_all("Supplier wise item",{'parent':supplier_item.name,},pluck="item_code")
        return supplier

@frappe.whitelist()
def item_customer(party_name):
    customer_item = frappe.get_doc("Customer",party_name)
    if(customer_item._default_item ==1):
        customer = frappe.get_all("Customer Default Items",{'parent':customer_item.name,},pluck="item_code")
        return customer
    
class GateEntry(Document):
    def on_submit(self):
        if self.against_po__dc == "DC Not for Sales" and self.is_gate_entry_in__out == "IN":

                # for i in self.items:
                #     frappe.db.set_value('DC Items', {
                #                         'parent': i.document_no,
                #                         'parenttype': self.against_po__dc,
                #                         'item_code': i.item_code
                #                         }, 'received_qty', i.received_qty)
                #     frappe.db.set_value('DC Items', {
                #                         'parent': i.document_no,
                #                         'parenttype': self.against_po__dc,
                #                         'item_code': i.item_code
                #                         }, 'balance_qty', i.balanced_qty)
                #     if i.balanced_qty == 0:
                #         frappe.db.set_value("DC Items", {
                #             'parent': i.document_no,
                #             'parenttype': self.against_po__dc,
                #             'item_code': i.item_code
                #             }, "total", 1)
                # document = frappe.new_doc("Stock Entry")
                # document.stock_entry_type ="Material Receipt"
                # document.to_warehouse = self.warehouse
                # document.dc_no = self.name,
                # for i in self.items:
                #     item = frappe.get_doc("Item",{"name":i.item_code})
                #     for j in item.uoms:
                #         if item.stock_uom == j.uom:
                #             document.append('items', dict(
                #                 item_code = i.item_code,
                #                 qty=i.received_qty,
                #                 basic_rate=1,
                #                 stock_uom = item.stock_uom,
                #                 uom=i.uom,
                #                 transfer_qty=i.received_qty,
                #                 conversion_factor = j.conversion_factor
                #             ))
                # document.save(ignore_permissions=True)
                # document.submit()

# Gate Entry to GRN Automate Creation - Draft Stage:------
                document = frappe.new_doc("GRN")
                document.party_type =self.party_type
                document.party =self.party_name
                document.party_name = self.party_name
                document.warehouse = grn_on_insert(self.party_name)
                document.gate_entry = self.name
                document.received_doc_no = self.document_no
                document.customer_address = grn_address_billing(self.party_type,self.party_name)
                document.shipping_address_name = grn_address_shipping(self.party_type,self.party_name)
                document.driver = self.driver_name
                document.vehicle_no = self.vehicle_no
                for i in self.items:
                    document.append('items', dict(
                        items = i.item_code,
                        item_name = i.item_name,
                        gate_entry_received_qty = i.received_qty, 
                        received_qty=i.received_qty,
                    ))
                document.save(ignore_permissions=True)
                self.status = "To GRN"
        elif self.against_po__dc == "Purchase Order" and self.is_gate_entry_in__out == "IN" and self.party_type == "Supplier":
                document = frappe.new_doc("GRN")
                document.party_type = "Supplier"
                document.purchase_order = "Purchase Order"
                document.party =self.party_name
                document.party_name = self.party_name
                document.received_doc_no = self.document_no
                document.warehouse = grn_on_insert(self.party_name)
                document.gate_entry = self.name
                document.customer_address = grn_address_billing(self.party_type,self.party_name)
                document.shipping_address_name = grn_address_shipping(self.party_type,self.party_name)
                document.driver = self.driver_name
                document.vehicle_no = self.vehicle_no
                for i in self.items:
                    document.append('items', dict(
                        items = i.item_code,
                        item_name = i.item_name,
                        gate_entry_received_qty = i.received_qty, 
                        received_qty=i.received_qty,
                    ))
                document.save(ignore_permissions=True)
                self.status = "To GRN"
        if self.against_po__dc == "Others" and self.is_gate_entry_in__out == "IN" and self.party_type == "Supplier":
                document = frappe.new_doc("Purchase Receipt")
                document.is_gate_entry = 1
                document.gate_entry = self.name,
                document.supplier =self.party_name
                for i in self.items:
                    document.append('items', dict(
                        item_code = i.item_code,
                        item_name = i.item_name,
                        qty=i.qty,
                        uom=i.uom,
                    ))
                document.save(ignore_permissions=True)
                self.status = "To Purchase Receipt"
    
    def on_cancel(self):
        # if self.against_po__dc == "DC Not for Sales" and self.is_gate_entry_in__out == "IN":
        #     for i in self.items:
        #         rec_qty = frappe.get_value("DC Items", {'parent': i.document_no,'parenttype':self.against_po__dc,'item_code':i.item_code},'received_qty') or 0
        #         frappe.db.set_value('DC Items', {'parent':  i.document_no,'parenttype':self.against_po__dc, 'item_code':i.item_code}, 'received_qty',float(rec_qty) - i.received_qty)
        #         frappe.db.set_value('DC Items', {'parent':  i.document_no,'parenttype':self.against_po__dc,'item_code':i.item_code}, 'balance_qty',i.balanced_qty + i.received_qty)
        #         frappe.db.set_value("DC Items", {"parent": i.document_no,'parenttype':self.against_po__dc,"item_code":i.item_code},"total",0)
        # if self.against_po__dc == "Purchase Order" and self.is_gate_entry_in__out == "IN":
            #  for i in self.items:
            #     rec_qty = frappe.get_value("Purchase Order Item", {'parent': i.document_no,'parenttype':self.against_po__dc,'item_code':i.item_code},'received_qty') or 0
            #     frappe.db.set_value('Purchase Order Item', {'parent':  i.document_no,'parenttype':self.against_po__dc, 'item_code':i.item_code}, 'received_qty',rec_qty - i.received_qty)
        if frappe.db.exists("Stock Entry",{"dc_no":self.name}):
            frappe.get_doc("Stock Entry",{"dc_no":self.name}).cancel()
        if frappe.db.exists("GRN",{"gate_entry":self.name}):
            frappe.get_doc("GRN",{"gate_entry":self.name}).cancel()
   
    def on_trash(self):
        if frappe.db.exists("Stock Entry",{"dc_no":self.name}):
            frappe.get_doc("Stock Entry",{"dc_no":self.name}).delete()
        if frappe.db.exists("GRN",{"gate_entry":self.name}):
            frappe.get_doc("GRN",{"gate_entry":self.name}).delete()
        if frappe.db.exists("Purchase Receipt",{"gate_entry":self.name}):
            frappe.get_doc("Purchase Receipt",{"gate_entry":self.name}).delete()
    def autoname(self):
        if(self.is_gate_entry_in__out == "OUT"):
            self.name = make_autoname(self.out,doc=self)