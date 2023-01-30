from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def material_request():
    material_requests_custom_fields()

def material_requests_custom_fields():
    material_requests_custom_fields = {
        'Material Request':[
            dict(
                fieldname='supplier_name_',
                fieldtype='Link',
                label = 'Supplier Name',
                options = 'Supplier',
                insert_after='material_request_type',
            ),  
        ],
    }
    create_custom_fields(material_requests_custom_fields)
    
    
def execute():
   material_request() 