from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def stock_entry():
    stock_entry_custom_fields()
    property_setter()
    
def stock_entry_custom_fields():
    stock_entry_custom_fields = {
        'Stock Entry':[
            dict(
                fieldname='suppliername',
                fieldtype='Link',
                label = 'Supplier',
                options='Supplier',
                insert_after='stock_entry_type',
            ),
        ],
    }
    create_custom_fields(stock_entry_custom_fields)

def property_setter():
    make_property_setter('Stock Entry', 'status', 'hidden', '1', 'Check')
    make_property_setter('Stock Entry', 'suppliername','depends_on',"eval:doc.stock_entry_type =='Material Transfer'",'Data')
   
   
def execute():
    stock_entry()
