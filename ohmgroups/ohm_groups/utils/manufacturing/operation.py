from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def operation():
    operation_custom_fields()
    # property_setter()
    
def operation_custom_fields():
    operation_custom_fields = {
        'Operation':[
            dict(
                fieldname='attributes',
                fieldtype='Link',
                label = 'Attributes',
                options = 'Ohm Item Attribute',
                insert_after='workstation',
            ),
        ],

    }
    create_custom_fields(operation_custom_fields)

# def property_setter():
#     make_property_setter('Sales Invoice', "naming_series", "options", ".####\nSI-.22-23.-.####\nSINV-.22-23.-\nSRET-.YY.-\nACC-SINV-.YYYY.-\nACC-SINV-RET-.YYYY.-", "Text")
#     make_property_setter('Sales Invoice', "naming_series", "default", ".####",'display_depends_on' "Text")
#     make_property_setter('Sales Invoice', "naming_series", "read_only", 1, "Check")

def execute():
    operation()
