# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

from argparse import Action
import json
import frappe
from frappe.model.document import Document

@frappe.whitelist()
def qc_check(qc, doctype, name, owner):
    user = frappe.db.get_value("User", owner, "username")
    emp_user = frappe.get_all("Employee",{'designation':"Quality"},"user_id")
    for i in emp_user:
        doc = frappe.new_doc('Notification Log')
        doc.update({
            'subject': f"From {doctype} Quality Inspection Created by {user} Now you check and submit the Quality Inspection",
            'for_user': i.user_id,
            'type': 'Alert',
            'document_type': doctype,
            'document_name': name,
            'from_user': owner,
            'email_content': "Quality Inspection Created"
        })
        doc.flags.ignore_permissions = True
        doc.insert()


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
    com_add = frappe.get_all("Dynamic Link", {"parenttype":"Address","link_doctype":"Company","link_name":company},pluck="parent")
    for i in com_add:
        com_plant_add =  frappe.get_value('Address',{'address_type':'Plant','name':i},"name")
        if com_plant_add:
            return com_plant_add
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
def grn_dc_items(items,company,party,party_type,purchase_order=None):
    item = json.loads(items)
    message = ""
    qty_taken = {l['items']:l['received_qty'] for l in item}
    po_qty_taken = {l['items']:l['received_qty'] for l in item}
    get_dc_all = frappe.get_all("DC Not for Sales",{"company":company,"party":party,"party_type":party_type,"docstatus":1},order_by='creation asc')
    get_po_all = frappe.get_all("Purchase Order",{"company":company,"naming_supplier":party,"docstatus":1},order_by='creation asc')
    dc_doc=[]
    po_doc=[]
    for k in item:
        if purchase_order:
            
            for po in get_po_all:
                
                get_po_doc = frappe.get_doc("Purchase Order",{"name":po.name})
                
                for j in get_po_doc.items:
                    if(j.item_code == k['items'] and j.qty - j.received_qty != 0 and po_qty_taken[k['items']]>0):
                       
                        qty=j.qty or 0
                        if(qty<= 0):
                            continue
                        if qty < po_qty_taken[k['items']]:
                            po_qty_taken[k['items']] -= qty
                            total = 0
                        elif qty >= po_qty_taken[k['items']]:
                            qty=po_qty_taken[k['items']]
                            po_qty_taken[k['items']] -= k['received_qty']
                            total = float(j.qty or 0) - qty
                        po_doc.append({"purchase_order_no":get_po_doc.name,"item_code":j.item_code,"item_name":j.item_name,"total_qty_in_dc":j.qty - j.received_qty or 0,"qty":qty,"dc_name":j.name,"balanced_qty":total})

        else:
            for i in get_dc_all:
                get_dc_doc = frappe.get_doc("DC Not for Sales",{"name":i.name})
                
                for j in get_dc_doc.items:
                    if (j.item_code == k['items'] and j.total == 0 and qty_taken[k['items']]>0):
                        qty=float(j.balance_qty or 0)
                        if(qty<= 0):
                            continue
                        if qty < qty_taken[k['items']]:
                            
                            qty_taken[k['items']] -= qty
                            tot = 0
                        elif qty >= qty_taken[k['items']]:
                            qty= qty_taken[k['items']]
                            qty_taken[k['items']] -= k['received_qty']
                            tot = float(j.balance_qty or 0) - qty 
                        dc_doc.append({"dc_no":get_dc_doc.name,"item_code":j.item_code,"total_qty_in_dc":float(j.balance_qty or 0),"qty":qty,"dc_name":j.name,"balanced_qty":tot})



    if purchase_order == "":
        for i in qty_taken:
            if (qty_taken[i] > 0):
                message += f"<p>{qty_taken[i]} Excess for {i}</p>"
            
    return dc_doc,message,po_doc 

@frappe.whitelist()
def create_inspection(items,name,gate_entry,party_type,party,received_doc_no):
    items = json.loads(items)
    doc_quality = []
    for i in items:
        if i.get('received_qty') !=0:
            if not i.get('inspection_doc') :
                document = frappe.new_doc("Quality Inspection")
                document.inspection_type = "Incoming"
                document.reference_type = "Others"
                document.party_type_ = party_type
                document.received_doc_no = received_doc_no
                document.party = party
                document.grn = name
                document.gate_entry = gate_entry
                document.sample_size = 1
                document.item_code = i.get("items")
                document.inspected_by = frappe.session.user
                document.save(ignore_permissions=True)
                doc_quality.append(document)
                frappe.db.set_value("GRN Items",i.get('name'),"inspection_doc",document.name)
                frappe.db.set_value("GRN",name,"status","QC Done")
                fetch_data(name, document)
            else:
                frappe.msgprint("Item Aginst Quality Inspection is Already Created")
    return doc_quality




def fetch_data(doc, document):
    doc = frappe.get_doc("GRN",doc)
    doc.append('quality_inspection_doc_no', dict(
        item_code = document.item_code,
        quality_inspection_doc_no=document.name,
        status=document.status


    ))
    doc.save()
from frappe.model.document import Document

class GRN(Document):
    def on_submit(self):
        for m in self.items:
            if m.inspection_doc in ["",None]:
                frappe.throw("Quality Inspection is Pending")
        for q in self.quality_inspection_doc_no:
            if q.inspection_list == 0 :
                frappe.throw("Kindly Check the All Quality Inspection")
            else:
                for i in self.dc_items:
                    if not self.purchase_order:
                        rec_qty = (frappe.get_value("DC Items", {'name': i.dc_name,'item_code':i.item_code},'received_qty') or 0)
                        frappe.db.set_value('DC Items', {'name': i.dc_name, 'item_code':i.item_code}, 'received_qty',float(rec_qty) + i.qty)
                        frappe.db.set_value('DC Items', {'name': i.dc_name, 'item_code':i.item_code}, 'balance_qty',i.balanced_qty)
                        if i.balanced_qty == 0:
                            frappe.db.set_value("DC Items", {"name":i.dc_name,"item_code":i.item_code},"total",1)
                    else:
                        rec_qty = (frappe.get_value("Purchase Order Item", {'name': i.dc_name,'parenttype':'Purchase Order','item_code':i.item_code},'received_qty') or 0)
                        frappe.db.set_value('Purchase Order Item', {'name': i.dc_name,'parenttype':'Purchase Order','item_code':i.item_code}, 'received_qty',rec_qty+i.qty )
        company = frappe.db.get_single_value("Global Defaults","default_company")
        abbr = frappe.db.get_value("Company",company,"abbr")
        document = frappe.new_doc("Stock Entry")
        document.stock_entry_type ="Material Receipt"
        document.to_warehouse = f"Stores - {abbr}"
        document.dc_no = self.name,
        for i in self.items:
                item = frappe.get_doc("Item",{"name":i.items})
                for j in item.uoms:
                    if item.stock_uom == j.uom:
                        document.append('items', dict(
                            item_code = i.items,
                            qty=i.received_qty,
                            basic_rate=1,
                            stock_uom = item.stock_uom,
                            uom=item.stock_uom,
                            transfer_qty=i.received_qty,
                            conversion_factor = j.conversion_factor
                        ))
        document.save(ignore_permissions=True)
        document.submit()
                
        
    
    def on_cancel(self):
        for i in self.dc_items:
            if not self.purchase_order:
                rec_qty = frappe.get_value("DC Items", {'name':i.dc_name,'item_code':i.item_code},'received_qty') or 0
                frappe.db.set_value('DC Items', {'name': i.dc_name, 'item_code':i.item_code}, 'received_qty',float(rec_qty) - i.qty)
                frappe.db.set_value('DC Items', {'name': i.dc_name, 'item_code':i.item_code}, 'balance_qty',i.balanced_qty + i.qty)            
                frappe.db.set_value("DC Items", {"name":i.dc_name,"item_code":i.item_code},"total",0)
            else:
                rec_qty = frappe.get_value("Purchase Order Item", {'name': i.dc_name,'parenttype':'Purchase Order','item_code':i.item_code},'received_qty') or 0
                frappe.db.set_value('Purchase Order Item', {'name':  i.dc_name,'parenttype':'Purchase Order', 'item_code':i.item_code}, 'received_qty',rec_qty - i.qty)


        # if frappe.db.exists("Quality Inspection",{"grn":self.name}):
        #     frappe.get_doc("Quality Inspection",{"grn":self.name}).cancel()
        if frappe.db.exists("Stock Entry",{"dc_no":self.name}):
            frappe.get_doc("Stock Entry",{"dc_no":self.name}).cancel()  

    def on_trash(self):
        # if frappe.db.exists("Quality Inspection",{"grn":self.name}):
        #     frappe.get_doc("Quality Inspection",{"grn":self.name}).delete()    
        if frappe.db.exists("Stock Entry",{"dc_no":self.name}):
            frappe.get_doc("Stock Entry",{"dc_no":self.name}).delete()    
	

# def qc_check(self):
#     frappe.set_value("GRN","quality_inspection","qc",1)