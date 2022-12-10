from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def quality_inspection():
    quality_inspection_custom_fields()
    property_setter()
    
def quality_inspection_custom_fields():
    quality_inspection_custom_fields = {
        'Quality Inspection':[
            dict(
                fieldname='section_break1',
                fieldtype='Section Break',
                insert_after='readings',
            ),
            dict(
                fieldname='sample_1',
                fieldtype='Data',
                insert_after='section_break1',
                label="Sample 1",
                read_only=1
            ),
            dict(
                fieldname='sample_2',
                fieldtype='Data',
                insert_after='sample_1',
                label="Sample 2",
                read_only=1
            ),
            dict(
                fieldname='sample_3',
                fieldtype='Data',
                insert_after='sample_2',
                label="Sample 3",
                read_only=1
            ),
            dict(
                fieldname='sample_4',
                fieldtype='Data',
                insert_after='sample_3',
                label="Sample 4",
                read_only=1
            ),
            dict(
                fieldname='col_1',
                fieldtype='Column Break',
                insert_after='sample_4',
            ),
            dict(
                fieldname='sample_5',
                fieldtype='Data',
                insert_after='col_1',
                label="Sample 5",
                read_only=1
            ),
            dict(
                fieldname='sample_6',
                fieldtype='Data',
                insert_after='sample_5',
                label="Sample 6",
                read_only=1
            ),
            dict(
                fieldname='sample_7',
                fieldtype='Data',
                insert_after='sample_6',
                label="Sample 7",
                read_only=1
            ),
            dict(
                fieldname='sample_8',
                fieldtype='Data',
                insert_after='sample_7',
                label="Sample 8",
                read_only=1
            ),
            dict(
                fieldname='col_2',
                fieldtype='Column Break',
                insert_after='sample_8',
            ),
            dict(
                fieldname='sample_9',
                fieldtype='Data',
                insert_after='col_2',
                label="Sample 9",
                read_only=1
            ),
            dict(
                fieldname='sample_10',
                fieldtype='Data',
                insert_after='sample_9',
                label="Sample 10",
                read_only=1
            ),
            
           
        ],
    }
    create_custom_fields(quality_inspection_custom_fields)

def property_setter():
    make_property_setter('Quality Inspection', "status", "hidden", "1", "Check")
    make_property_setter('Quality Inspection', "sample_size", "label", "Sample Qty", "Data")
    

def execute():
    quality_inspection()
