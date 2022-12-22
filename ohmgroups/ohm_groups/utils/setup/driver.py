from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def driver_custom_fields():
    driver_custom_fields={
        "Driver":[
          dict(
          fieldname = "employee_categories",
          fieldtype = "Link",
          insert_after = "address",
          options = "Designation",
          label = "Employee Categories",
          ),
        ],
    }
    create_custom_fields(driver_custom_fields)
    
def execute():
  driver_custom_fields()