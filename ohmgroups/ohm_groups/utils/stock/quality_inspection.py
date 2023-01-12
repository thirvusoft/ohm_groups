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
            dict(
                fieldname='column_break_19',
                fieldtype='Column Break',
                insert_after='quality_inspection_template',
            ),
            dict(
                fieldname='is_parameter',
                fieldtype='Check',
                insert_after='column_break_19',
                label = 'Enter manual Data'
            ),
            dict(
                fieldname='section_break_21',
                fieldtype='Section Break',
                insert_after='is_parameter',
            ),
            dict(
                fieldname='inspection_report_name',
                fieldtype='Data',
                insert_after='report_date',
                label = 'Inspection Report Name',
            ),
            dict(
                fieldname='sec_break1',
                fieldtype='Section Break',
                insert_after='sample_10',
            ),
            dict(
                fieldname='equipments_1',
                fieldtype='Data',
                insert_after='sec_break1',
                default = 'VC- VERNIER CALIPER',
                label = 'Equipment 1',
                hidden = 1
            ),
                        dict(
                fieldname='column_break_20',
                fieldtype='Column Break',
                insert_after='equipments_1',
            ),
            dict(
                fieldname='equipments_2',
                fieldtype='Data',
                insert_after='column_break_20',
                default = 'VC-VERNIER CALIPER',
                label = 'Equipment 2',
                hidden = 1
        
            ),
                        dict(
                fieldname='column_break_21',
                fieldtype='Column Break',
                insert_after='equipments_2',
            ),
            dict(
                fieldname='equipments_3',
                fieldtype='Data',
                insert_after='column_break_21',
                default = 'PG-PLUG GAUGE',
                label = 'Equipment 3',
                hidden = 1
        
            ),
                        dict(
                fieldname='column_break_22',
                fieldtype='Column Break',
                insert_after='equipments_3',
            ),
            dict(
                fieldname='equipments_4',
                fieldtype='Data',
                insert_after='column_break_22',
                default = 'BP-BEVEL PROPTER',
                label = 'Equipment 4',
                hidden = 1
            ),
        dict(
                fieldname='column_break_23',
                fieldtype='Column Break',
                insert_after='equipments_4',
        ),
            dict(
                fieldname='equipments_5',
                fieldtype='Data',
                insert_after='column_break_23',
                default = 'MT-MEASUREING TAPE',
                label = 'Equipment 5',
                hidden = 1
            ),
        dict(
                fieldname='column_break_24',
                fieldtype='Column Break',
                insert_after='equipments_5',
        ),
            dict(
                fieldname='equipments_6',
                fieldtype='Data',
                insert_after='column_break_24',
                default = 'HG-HEIGHT GAUGE',
                label = 'Equipment 5',
                hidden = 1
            ),
        ],
    }
    create_custom_fields(quality_inspection_custom_fields)

def property_setter():
    make_property_setter('Quality Inspection', "status", "hidden", "1", "Check")
    make_property_setter('Quality Inspection', "sample_size", "label", "Sample Qty", "Data")
    make_property_setter('Quality Inspection', "reference_type", "options", "\nPurchase Receipt\nPurchase Invoice\nDelivery Note\nSales Invoice\nStock Entry\nJob Card\nOthers", "Text")
    make_property_setter('Quality Inspection', "reference_name", "mandatory_depends_on", "eval:doc.reference_type!='Others'", "Text")
    make_property_setter('Quality Inspection', "reference_name", "reqd", "0", "Check")
    

def execute():
    quality_inspection()
