from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def sales_invoice():
    sales_invoice_custom_fields()
    property_setter()
    
def sales_invoice_custom_fields():
    sales_invoice_custom_fields = {
        'Sales Invoice':[
            dict(
                fieldname='vendor_code',
                fieldtype='Data',
                label = 'Vendor Code',
                fetch_from = 'customer.vendor_code',
                insert_after='customer',
            ),

        ],
    }
    create_custom_fields(sales_invoice_custom_fields)

def property_setter():
    pass
    # make_property_setter('Quality Inspection', "status", "hidden", "1", "Check")
    # make_property_setter('Quality Inspection', "sample_size", "label", "Sample Qty", "Data")
    

def execute():
    sales_invoice()
