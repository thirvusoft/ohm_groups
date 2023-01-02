from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def quality_inspection_paramter():
    quality_inspection_paramter_custom_fields()

def quality_inspection_paramter_custom_fields():
    quality_inspection_paramter_custom_fields = {
        'Item Quality Inspection Parameter':[
            dict(
                fieldname='si_no',
                fieldtype='Data',
                label = 'Si No',
                insert_after='specification',
            ), 

            dict(
                fieldname='testing_type',
                fieldtype='Link',
                label = 'Testing Type',
                options = 'Testing Type',
                insert_after='acceptance_formula',
            ),   
        ],
    }
    create_custom_fields(quality_inspection_paramter_custom_fields)
    
    
def property_setter():
    pass
    make_property_setter('Item Quality Inspection Parameter', "reading_1", "label", "Sample 1", "Data")
def execute():
   quality_inspection_paramter() 