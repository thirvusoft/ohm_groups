from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def stock_entry():
    stock_entry_custom_fields()
    property_setter()
    
def stock_entry_custom_fields():
    stock_entry_custom_fields = {
        'Stock Entry':[
            dict(
                fieldname='suppliername',
                fieldtype='Link',
                label = 'Subcontractor',
                options='Supplier',
                insert_after='stock_entry_type',
            ),
            dict(
                fieldname='e_way_bill',
                fieldtype='Data',
                insert_after='suppliername',
                label="E-way bill",
                depends_on= "eval:doc.suppliername" 
            ), 
            dict(
                fieldname='po_no',
                fieldtype='Data',
                insert_after='e_way_bill',
                label="Supplier So No",
                depends_on= "eval:doc.suppliername"  
            ), 
            dict(
                fieldname='po_date',
                fieldtype='Date',
                insert_after='po_no',
                label="Supplier So Date",
                depends_on = "eval:doc.suppliername"  
            ), 

            dict(
                fieldname='transport_info',
                fieldtype='Section Break',
                insert_after='total_additional_costs',
                label="Transport Info",
                collapsible = 1
            ), 

            dict(
                fieldname='driver',
                fieldtype='Link',
                insert_after='transport_info',
                label="Driver",
                options="Driver",
            ), 

            dict(
                fieldname='driver_name',
                fieldtype='Data',
                insert_after='driver',
                label="Driver Name",
                fetch_from="driver.full_name",
            ), 

            dict(
                fieldname='vehicle_no',
                fieldtype='Data',
                insert_after='driver_name',
                label="Vehicle No",
            ), 

        ],
    }
    create_custom_fields(stock_entry_custom_fields)

def property_setter():
    make_property_setter('Stock Entry', 'status', 'hidden', '1', 'Check')
    make_property_setter('Stock Entry', 'suppliername','depends_on',"eval:doc.stock_entry_type =='Material Transfer'",'Data')
   
   
def execute():
    stock_entry()
