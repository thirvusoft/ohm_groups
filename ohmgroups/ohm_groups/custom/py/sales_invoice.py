import frappe

# @frappe.whitelist()
# def item_customers(customer):
#     customer_item = frappe.get_doc("Customer",customer)
#     if(customer_item._default_item ==1):
#         customer = frappe.get_all("Customer Default Items",{'parent':customer_item.name,},pluck="item_code")
#         return customer
    
def to_grn(doc,actions):
        document_dc = frappe.new_doc("Gate Entry")
        document_dc.is_gate_entry_in__out = "OUT"
        document_dc.party_type = "Customer"
        document_dc.party_name = doc.customer
        document_dc.branch = doc.branch
        document_dc.po_no = doc.po_no
        document_dc.po_date = doc.po_date
        document_dc.against_si__dc = doc.doctype 
        document_dc.driver = doc.driver
        document_dc.si_doc_no = doc.name
        document_dc.vehicle_no = doc.vehicle_no
        document_dc.append('sales_invoice', dict(
        goods_received_from = doc.name))
        document_dc.save(ignore_permissions=True)

def trash(doc,actions):
       if frappe.db.exists("Gate Entry",{"si_doc_no":doc.name}):
             frappe.get_doc("Gate Entry",{"si_doc_no":doc.name}).delete()