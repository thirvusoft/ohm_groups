from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
def batch_customizations():
    batch_custom_fields()
    batch_property_setter()
def batch_custom_fields():
    custom_fields = {
        "Vehicle": [
            dict(
                fieldname="is_add_on",
                fieldtype="Check",
                label="Is Add-on",
                insert_after="model"
            ),
            dict(
                fieldname="add_on",
                fieldtype="Link",
                label="Add-On",
                insert_after="make",
                options="Vehicle",
				depends_on="eval:doc.is_add_on == 1 "
            ),
            dict(
                fieldname="costing_details",
                fieldtype="Section Break",
                label="Costing Details",
                insert_after="employee11",
            ),
            dict(
                fieldname="maintenance_cost",
                fieldtype="Float",
                label="Maintenance Cost Per Km",
                insert_after="costing_details",
            ),
            dict(
                fieldname="driver_cost",
                fieldtype="Float",
                label="Driver Cost",
                insert_after="maintenance_cost",
            ),
            dict(
                fieldname="column_break_18",
                fieldtype="Column Break",
                insert_after="driver_cost",
            ),
            dict(
                fieldname="mileage",
                fieldtype="Float",
                label="Mileage",
                insert_after="column_break_18",
            ),
            dict(
                fieldname="operator",
                fieldtype="Link",
                label="Operator",
                options="Driver",
                insert_after="acquisition_date",
            ),
            dict(
                fieldname="employee1",
                fieldtype="Link",
                label="Driver",
                options = "Driver",
                insert_after="vehicle_value",
            ),
            dict(
                fieldname="employee11",
                fieldtype="Data",
                label="Employee",
                insert_after="employee1",
                translatable = 1,
                fetch_from = "employee1.employee"
            ),
            dict(
                fieldname="section_break_28",
                fieldtype="Section Break",
                label="Maintanence Details ",
                insert_after="doors",
            ),
            dict(
                fieldname="maintanence_details_",
                fieldtype="Table",
                insert_after="section_break_28",
                options="Maintenance Details"
            ),
            dict(
                fieldname="expiration_dates",
                fieldtype="Section Break",
                label="Expiration Dates",
                insert_after="maintanence_details_",
            ),
            dict(
                fieldname="insurance_expired_date",
                fieldtype="Date",
                label="Insurance Expired Date",
                insert_after="expiration_dates",
                read_only=1,
            ),
            dict(
                fieldname="fc_details_expired_date",
                fieldtype="Date",
                label="FC Details Expired Date",
                insert_after="insurance_expired_date",
                read_only=1,
            ),
            dict(
                fieldname="road_tax_expired_date",
                fieldtype="Date",
                label="Road Tax Expired Date",
                insert_after="fc_details_expired_date",
                read_only=1,
            ),
            dict(
                fieldname="column_break_32",
                fieldtype="Column Break",
                insert_after="road_tax_expired_date",
            ),
            dict(
                fieldname="permit_expired_date",
                fieldtype="Date",
                label="Permit Expired Date",
                insert_after="column_break_32",
                read_only=1,
            ),
            dict(
                fieldname="pollution_certificate_expired_date",
                fieldtype="Date",
                label="Pollution Certificate Expired Date",
                insert_after="permit_expired_date",
                read_only=1,
            ),
            dict(
                fieldname="green_tax_expired_date",
                fieldtype="Date",
                label="Green Tax Expired Date",
                insert_after="pollution_certificate_expired_date",
                read_only=1,
            ),
            dict(
                fieldname="add_on_details",
                fieldtype="Section Break",
                label="Add On Details",
                hidden=1,
                insert_after="green_tax_expired_date",

            ),
            dict(
                fieldname="make_1",
                fieldtype="Data",
                label="Make",
                insert_after="add_on_details",
                translatable =1,
            ),
            dict(
                fieldname="model_1",
                fieldtype="Data",
                label="Model",
                insert_after="make_1",
                translatable =1,
            ),
            dict(
                fieldname="service_details",
                fieldtype="Section Break",
                label="Service Details",
                insert_after="model_1",
            ),
            dict(
                fieldname="service_details_table",
                fieldtype="Table",
                insert_after="service_details",
                options="TS Vehicle Service"
            ),

            ]
    }
    create_custom_fields(custom_fields)
def batch_property_setter():                
    make_property_setter("Vehicle", "add_on_details", "hidden", "1", "Check")
    make_property_setter("Vehicle", "location", "hidden", "1", "Check")
    make_property_setter("Vehicle", "employee", "hidden", "1", "Check")


def execute():
  batch_customizations()