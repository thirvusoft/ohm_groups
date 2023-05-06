from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def purchase_receipt():
    purchase_receipt_custom_fields()
    property_setter()
    
def purchase_receipt_custom_fields():
    pass
    # purchase_receipt_custom_fields = {
    #     'Purchase Receipt':[

    #         dict(
    #             fieldname='naming_supplier',
    #             fieldtype='Link',
    #             insert_after='naming_series',
    #             label="Supplier",
    #             options="Supplier",
    #             reqd = 1
    #         ), 

    #         dict(
    #             fieldname='e_way_bill',
    #             fieldtype='Data',
    #             insert_after='supplier_warehouse',
    #             label="E-way bill",
    #             depends_on= "eval:doc.is_subcontracted == 1" 
    #         ), 
    #         dict(
    #             fieldname='po_no',
    #             fieldtype='Data',
    #             insert_after='schedule_date',
    #             label="Supplier So No",
    #             depends_on= "eval:doc.is_subcontracted == 1" 
    #         ), 
    #         dict(
    #             fieldname='po_date',
    #             fieldtype='Date',
    #             insert_after='po_no',
    #             label="Supplier So Date",
    #             depends_on = "eval:doc.is_subcontracted == 1" 
    #         ), 

    #         dict(
    #             fieldname='transport_info',
    #             fieldtype='Section Break',
    #             insert_after='more_info_tab',
    #             label="Transport Info",
    #             collapsible = 1
    #         ), 

    #         dict(
    #             fieldname='driver',
    #             fieldtype='Link',
    #             insert_after='transport_info',
    #             label="Driver",
    #             options="Driver",
    #         ), 
    #         dict(
    #             fieldname='mode_of_delivery',
    #             fieldtype='Select',
    #             insert_after='driver',
    #             label="Mode of Delivery",
    #             options="By Road\nSea\nTrain\nAir",
    #         ), 
    #         dict(
    #             fieldname='driver_name',
    #             fieldtype='Data',
    #             insert_after='driver',
    #             label="Driver Name",
    #             fetch_from="driver.full_name",
    #         ), 

    #         dict(
    #             fieldname='vehicle_no',
    #             fieldtype='Data',
    #             insert_after='driver_name',
    #             label="Vehicle No",
    #         ), 
    #         dict(
    #             fieldname='dc_no',
    #             fieldtype='Data',
    #             insert_after='naming_supplier',
    #             label="Delivery Challan",
    #         ), 
    #     ],
    # }
    # create_custom_fields(purchase_order_custom_fields)

def property_setter():
    make_property_setter('Purchase Receipt', "status", "options", "\nDraft\nTo Bill\nCompleted\nReturn Issued\nCancelled\nClosed\nQC Pending\nQC Checked", "Text Editor")
  

def execute():
    purchase_receipt()
