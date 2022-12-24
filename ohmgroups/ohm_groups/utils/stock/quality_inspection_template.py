from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def quality_inspection_template():
    quality_inspection_template_custom_fields()
    property_setter()

def quality_inspection_template_custom_fields():
    quality_inspection_template_custom_fields = {
        'Quality Inspection Template':[
            dict(
                fieldname='item_name',
                fieldtype='Link',
                label = 'Item Name',
                options = "Item",
                insert_after='quality_inspection_template_name',
            ),  
            dict(
                fieldname='item_image',
                fieldtype='Attach',
                label = 'Image',
                insert_after='quality_inspection_template_name',
            ),  
        ],
    }
    create_custom_fields(quality_inspection_template_custom_fields)
    
def property_setter():
    pass

def execute():
   quality_inspection_template() 