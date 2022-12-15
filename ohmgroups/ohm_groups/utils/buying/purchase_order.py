from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def purchase_order():
    purchase_order_custom_fields()
    property_setter()
    
def purchase_order_custom_fields():
    purchase_order_custom_fields = {
        'Purchase Order':[

            dict(
                fieldname='naming_supplier',
                fieldtype='Link',
                insert_after='naming_series',
                label="Supplier Name",
                options="Supplier"
            ), 
           
        ],
    }
    create_custom_fields(purchase_order_custom_fields)

def property_setter():
    pass
    

def execute():
    supplier()
