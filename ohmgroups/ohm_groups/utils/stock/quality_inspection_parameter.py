from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

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
        ],
    }
    create_custom_fields(quality_inspection_paramter_custom_fields)
    
def execute():
   quality_inspection_paramter() 