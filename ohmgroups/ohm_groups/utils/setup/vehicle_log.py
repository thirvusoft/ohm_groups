from frappe import read_only
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def batch_customization():
    batch_custom_fields()
    batch_property_setter()
def batch_custom_fields():
    custom_fields = {
        "Vehicle Log": [
            dict(
                fieldname="select_purpose",
                fieldtype="Select",
                label="Purpose",
                insert_after="today_odometer_value",
                options="\nFuel\nRaw Material\nService\nGoods Supply"
            ),
            dict(
                fieldname="mileage",
                fieldtype="Float",
                label="Mileage",
                insert_after="purchase_invoice",
                fetch_from = "license_plate.mileage",
                read_only = 1
            ),
            dict(
                fieldname="total_hours_travelled",
                fieldtype="Float",
                label="Total Hours Travelled",
                insert_after="mileage",
            ),
            dict(
                fieldname="sales_invoice",
                fieldtype="Link",
                label="Sales Invoice",
                insert_after="odometer",
                options="Sales Invoice",
                depends_on="eval:doc.select_purpose == 'Goods Supply' "
            ),
            dict(
                fieldname="purchase_invoice",
                fieldtype="Link",
                label="Purchase Invoice",
                insert_after="odometer",
                options="Purchase Invoice",
                depends_on="eval:doc.select_purpose == 'Raw Material' "
            ),
            dict(
                fieldname="purchase_receipt",
                fieldtype="Link",
                label="Purchase Receipt",
                insert_after="select_purpose",
                options="Purchase Receipt",
                depends_on="eval:doc.select_purpose == 'Raw Material' "
            ),
            dict(
                fieldname="service_item_table",
                fieldtype="Table",
                label="Service Item",
                insert_after="service_detail",
                options="Vehicle Log Service"
            ),
            dict(
                fieldname="today_odometer_value",
                fieldtype="Float",
                label="Distance Travelled",
                insert_after="last_odometer",
                read_only = 1,
            ),
            dict(
                fieldname="delivery_note",
                fieldtype="Link",
                label="Delivery Note",
                insert_after="purchase_receipt",
                options = "Delivery Note",
                depends_on = "eval:doc.select_purpose == 'Goods Supply' "
            ),
            dict(
                fieldname="purpose",
                fieldtype="Data",
                label="Purpose",
                hidden = 1,
                insert_after="delivery_note",
                transalatable = 1,
            ),
            dict(
                fieldname="section_break_18",
                fieldtype="Section Break",
                label="Costing Details",
                insert_after="purpose",
            ),
            dict(
                fieldname="ts_driver_cost",
                fieldtype="Float",
                label="Ts driver cost",
                hidden =1,
                fetch_from = "license_plate.driver_cost",
                insert_after="section_break_18",
            ),
            dict(
                fieldname="driver_cost",
                fieldtype="Float",
                label="Driver Cost",
                insert_after="ts_driver_cost",
            ),
            dict(
                fieldname="column_break_21",
                fieldtype="Column Break",
                insert_after="driver_cost",
            ),
            dict(
                fieldname="ts_total_cost",
                fieldtype="Float",
                label = "Total Cost",
                insert_after="column_break_21",
                read_only = 1
            ),
            dict(
                fieldname="total_fuel",
                fieldtype="Float",
                label = "Total fuel",
                insert_after="price",
                read_only = 1
            ),
            dict(
                fieldname="supplier1",
                fieldtype="Link",
                label = "Supplier",
                insert_after="service_detail",
                options = "Supplier",
            ),
            dict(
                fieldname="total_expence",
                fieldtype="Float",
                label = "Total expense service",
                insert_after="service_item_table",
                read_only = 1,
            ),
            dict(
                fieldname="add_on_service_details",
                fieldtype="Section Break",
                label = "Add On Service Details",
                insert_after="total_expence",
                hidden = 1,
            ),
            dict(
                fieldname="add_on_service_detail",
                fieldtype="Table",
                options = "Vehicle Service",
                insert_after="add_on_service_details",
            ),
            dict(
                fieldname="section_break_21",
                fieldtype="Section Break",
                label = "Maintanence Details",
                insert_after="add_on_service_detail",
            ),
            dict(
                fieldname="supplier2",
                fieldtype="Link",
                label = "Supplier",
                options = "Supplier",
                insert_after="section_break_21",
            ),
            dict(
                fieldname="maintanence_details",
                fieldtype="Table",
                options = "Maintenance Details",
                insert_after="supplier2",
            ),
            dict(
                fieldname="total_expence_maintanence",
                fieldtype="Float",
                label = "Total Expense Maintanence",
                insert_after="maintanence_details",
                read_only =1
            ),
            dict(
                fieldname="total_vehicle_costs",
                fieldtype="Float",
                label = "Total vehicle log cost",
                insert_after="total_expence_maintanence",
                read_only =1
            ),




            ]
    }
    create_custom_fields(custom_fields)
def batch_property_setter():                
    make_property_setter("Vehicle Log", "add_on_service_details", "hidden", "1", "Check")
    make_property_setter("Vehicle Service", "frequency", "reqd", "0", "Check")
    make_property_setter("Vehicle Service", "frequency", "hidden", "1", "Check")
    make_property_setter("Vehicle Log", "service_detail", "hidden", "1", "Check")
    make_property_setter("Vehicle Log", "today_odometer_value", "label", "Distance Travelled", "Data")
    make_property_setter("Vehicle Log", "today_odometer_value", "read_only", "1", "Check")
    make_property_setter("Vehicle Log", "select_purpose", "reqd", "1", "Check")
    make_property_setter("Vehicle Log", "employee", "fetch_from", "license_plate.employee11", "Text Editor")

def execute():
  batch_customization()