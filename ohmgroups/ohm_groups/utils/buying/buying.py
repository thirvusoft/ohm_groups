from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def supplier():
    supplier_custom_fields()
    property_setter()
    
def supplier_custom_fields():
    supplier_custom_fields = {
        'Supplier':[
            dict(
                fieldname='column_break61',
                fieldtype='Column Break',
                insert_after='default_bank_account',
            ), 
            dict(
                fieldname='default_item',
                fieldtype='Check',
                insert_after='tax_withholding_category',
                label ='Default Item',
            ), 
            dict(
                fieldname='section_break61',
                fieldtype='Section Break',
                insert_after='default_item',
            ), 
            dict(
                fieldname='supplier_item',
                fieldtype='Table',
                insert_after='section_break61',
                label ='Supplier Item',
                options = 'Supplier wise item'
            ),   
        ],
    }
    create_custom_fields(supplier_custom_fields)

def property_setter():
    pass
    

def execute():
    supplier()
