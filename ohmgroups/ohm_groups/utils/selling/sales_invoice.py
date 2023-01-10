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
        'Sales Invoice Item' :[
            dict(
                fieldname = 'desc',
                fieldtype='Text Editor',
                label='Desc',
                insert_after='description_section'
            ),

        ]
    }
    create_custom_fields(sales_invoice_custom_fields)

def property_setter():
    make_property_setter('Sales Invoice', "naming_series", "options", "SINV-.22-23.-\nSRET-.YY.-\nACC-SINV-.YYYY.-\nACC-SINV-RET-.YYYY.-", "Text")
    make_property_setter('Sales Invoice', "naming_series", "default", "SINV-.22-23.-", "Text")
    make_property_setter('Sales Invoice', "naming_series", "read_only", 1, "Check")

    

def execute():
    sales_invoice()
