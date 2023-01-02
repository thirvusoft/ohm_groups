from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def purchase_order():
    purchase_order_custom_fields()
    property_setter()
    
def purchase_order_custom_fields():
    purchase_order_custom_fields = {
        'Purchase Order':[

            dict(
                fieldname='naming_supplier',
                fieldtype='Link',
                insert_after='naming_series',
                label="Supplier",
                options="Supplier",
                reqd = 1
            ), 

            dict(
                fieldname='e_way_bill',
                fieldtype='Data',
                insert_after='supplier_warehouse',
                label="E-way bill",
                depends_on= "eval:doc.is_subcontracted == 1" 
            ), 
            dict(
                fieldname='po_no',
                fieldtype='Data',
                insert_after='schedule_date',
                label="Supplier So No",
                depends_on= "eval:doc.is_subcontracted == 1" 
            ), 
            dict(
                fieldname='po_date',
                fieldtype='Date',
                insert_after='po_no',
                label="Supplier So Date",
                depends_on = "eval:doc.is_subcontracted == 1" 
            ), 

            dict(
                fieldname='transport_info',
                fieldtype='Section Break',
                insert_after='more_info_tab',
                label="Transport Info",
                depends_on="eval:doc.is_subcontracted ==1",
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
            dict(
                fieldname='dc_no',
                fieldtype='Data',
                insert_after='naming_supplier',
                label="Delivery Challan",
            ), 
        ],

    }
    create_custom_fields(purchase_order_custom_fields)

def property_setter():
    make_property_setter('Purchase Order', "supplier", "reqd", 0, "Check")
    make_property_setter('Purchase Order', "supplier", "hidden", 1, "Check")
    make_property_setter('Purchase Order', "supplier_name", "fetch_from", "naming_supplier.supplier_name", "Text Editor")
    make_property_setter('Purchase Order Item','item_code','label','Process','Data')
    make_property_setter('Purchase Order','set_warehouse','depends_on','eval:doc.is_subcontracted !=1','Data')
    

def execute():
    purchase_order()
