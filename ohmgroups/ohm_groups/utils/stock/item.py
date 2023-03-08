from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def item():
    item_custom_fields
    property_setter()

def item_custom_fields():
    pass
def property_setter():
    make_property_setter('Item', "valuation_rate", "default", 1, "Text Editor")

def execute():
    item() 