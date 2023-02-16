from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def bom():
    bom_custom_fields()
    # property_setter()
    
def bom_custom_fields():
    bom_custom_fields = {

        'BOM Operation':[
            dict(
                fieldname='seq_id',
                fieldtype='Int',
                label = 'Seq Id',
                insert_after='sequence_id',
            ),
        ],
        'BOM Item':[
            dict(
                fieldname='job_',
                fieldtype='Check',
                label = 'Seprate Job Card',
                insert_after='item_name',
            ),
        ],
    }
    create_custom_fields(bom_custom_fields)

# def property_setter():
#     make_property_setter('Sales Invoice', "naming_series", "options", ".####\nSI-.22-23.-.####\nSINV-.22-23.-\nSRET-.YY.-\nACC-SINV-.YYYY.-\nACC-SINV-RET-.YYYY.-", "Text")
#     make_property_setter('Sales Invoice', "naming_series", "default", ".####",'display_depends_on' "Text")
#     make_property_setter('Sales Invoice', "naming_series", "read_only", 1, "Check")

def execute():
    bom()
