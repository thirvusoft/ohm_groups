from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def salary_structure_assignment():
    salary_structure_assignment_custom_fields()
    property_setter()
    
def salary_structure_assignment_custom_fields():
        salary_structure_assignment_custom_fields = {
        'Employee':[
            dict(
                fieldname='total_count_',
                fieldtype='Int',
                label = 'Total Count',
                insert_after='salutation',
            ),
        ],
        'Employee Checkin':[
            dict(
                fieldname='designation',
                fieldtype='Data',
                label = 'Designation',
                insert_after='employee',
                read_only=1,
                fetch_from ="employee.designation"
            ),
        ],
        'Salary Structure Assignment':[
            dict(
                fieldname='total_count_',
                fieldtype='Int',
                label = 'Total Count',
                insert_after='section_break_7',
                read_only=1,
                hidden =1,
                fetch_from ="employee.total_count_"
            ),
        ],
        'Salary Slip':[
            dict(
                fieldname='total_count_',
                fieldtype='Int',
                label = 'Total Count',
                insert_after='payroll_frequency',
                read_only=1,
                hidden =1,
                fetch_from ="employee.total_count_"
            ),
        ],
    }
        create_custom_fields(salary_structure_assignment_custom_fields)
    
def property_setter():
    make_property_setter("Salary Structure Assignment", "base", "label", "Wages", "Data")
    make_property_setter("Salary Structure Assignment", "from_date", "fetch_from", "employee.date_of_joining", "Data")
    make_property_setter("Salary Structure Assignment", "variable", "hidden", 1, "Check")
    make_property_setter("Salary Structure Assignment", "company", "fetch_from", "employee.company", "Data")
    

def execute():
    salary_structure_assignment()
