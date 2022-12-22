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
                label="Supplier",
                options="Supplier",
                reqd = 1
            ), 
           
        ],

    }
    create_custom_fields(purchase_order_custom_fields)

def property_setter():
    make_property_setter('Purchase Order', "supplier", "reqd", 0, "Check")
    make_property_setter('Purchase Order', "supplier", "hidden", 1, "Check")
    make_property_setter('Purchase Order', "supplier_name", "fetch_from", "naming_supplier.supplier_name", "Text Editor")
    make_property_setter('Purchase Order Item','item_code','label','Process','Data')
    

def execute():
    purchase_order()
