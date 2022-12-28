from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def salary_structure_assignment():
    salary_structure_assignment_custom_fields()
    property_setter()
    
def salary_structure_assignment_custom_fields():
    pass

def property_setter():
    make_property_setter("Salary Structure Assignment", "base", "label", "Wages", "Data")
    make_property_setter("Salary Structure Assignment", "from_date", "fetch_from", "employee.date_of_joining", "Data")
    make_property_setter("Salary Structure Assignment", "variable", "hidden", 1, "Check")
    make_property_setter("Salary Structure Assignment", "company", "fetch_from", "employee.company", "Data")
    

def execute():
    salary_structure_assignment()
