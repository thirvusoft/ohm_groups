from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def branch():
    branch_custom_fields()
    property_setter()
    
def branch_custom_fields():
    branch_custom_fields = {
        'Branch':[
            dict(
                fieldname='address',
                fieldtype='Link',
                label='Address',
                options='Address',
                insert_after='branch',
            ), 
            dict(
                fieldname='company',
                fieldtype='Link',
                insert_after='address',
                options='Company',
                label ='Company',
            ), 
            dict(
                fieldname='warehouse',
                fieldtype='Data',
                insert_after='company',
                label ='Branch Warehouse',
            ), 
        ],
    }
    create_custom_fields(branch_custom_fields)

def property_setter():
    pass
    

def execute():
    branch()
