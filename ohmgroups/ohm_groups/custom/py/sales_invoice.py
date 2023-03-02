import frappe

@frappe.whitelist()
def item_customers(customer_name):
    customer_item = frappe.get_doc("Customer",customer_name)
    if(customer_item._default_item ==1):
        customer = frappe.get_all("Customer Default Items",{'parent':customer_item.name,},pluck="item_code")
        return customer