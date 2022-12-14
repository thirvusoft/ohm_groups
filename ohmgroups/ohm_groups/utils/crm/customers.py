from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def customers():
    customer_custom_fields()
    property_setter()
    
def customer_custom_fields():
    customer_custom_fields = {
        'Customer':[
            dict(
                fieldname='column_break11',
                fieldtype='Column Break',
                insert_after='customer_name',
            ),
            dict(
                fieldname='vendor_code',
                fieldtype='Data',
                insert_after='column_break11',
                label="Vendor Code",
            ),       
        ],
    }
    create_custom_fields(customer_custom_fields)

def property_setter():
    pass
    # make_property_setter('Quality Inspection', "status", "hidden", "1", "Check")
    # make_property_setter('Quality Inspection', "sample_size", "label", "Sample Qty", "Data")
    

def execute():
    customers()
