from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def delivery_note():
    delivery_note_custom_fields()
    property_setter()
    
def delivery_note_custom_fields():
    delivery_note_custom_fields = {
        'Delivery Note':[
            dict(
                fieldname='supplier',
                fieldtype='Link',
                label = 'Supplier',
                options = 'Supplier',
                insert_after='naming_series',
                depends_on = "eval:doc.is_subcontracted == 1",
            ),
            dict(
                fieldname='is_subcontracted',
                fieldtype='Check',
                label = 'is Subcontracted',
                fetch_from = 'customer.vendor_code',
                insert_after='is_return',
            ),
            dict(
                fieldname='supplier_warehouse',
                fieldtype='Data',
                label = 'Supplier Warehouse',
                depends_on = "eval:doc.is_subcontracted == 1",
                insert_after='is_subcontracted',
                read_only = 1
            ),
            

        ],
    }
    create_custom_fields(delivery_note_custom_fields)

def property_setter():
    pass
    make_property_setter('Delivery Note', "customer", "depends_on", "eval:doc.is_subcontracted != 1", "Data")
    make_property_setter('Delivery Note', "customer", "reqd", "0", "Check")
    

def execute():
    delivery_note()
