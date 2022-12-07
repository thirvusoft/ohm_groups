from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def property_setter():
    make_property_setter('Quality Inspection Reading', "reading_1", "label", "Sample 1", "Data")
    make_property_setter('Quality Inspection Reading', "reading_2", "label", "Sample 2", "Data")
    make_property_setter('Quality Inspection Reading', "reading_3", "label", "Sample 3", "Data")
    make_property_setter('Quality Inspection Reading', "reading_4", "label", "Sample 4", "Data")
    make_property_setter('Quality Inspection Reading', "reading_5", "label", "Sample 5", "Data")
    make_property_setter('Quality Inspection Reading', "reading_6", "label", "Sample 6", "Data")
    make_property_setter('Quality Inspection Reading', "reading_7", "label", "Sample 7", "Data")
    make_property_setter('Quality Inspection Reading', "reading_8", "label", "Sample 8", "Data")
    make_property_setter('Quality Inspection Reading', "reading_9", "label", "Sample 9", "Data")
    make_property_setter('Quality Inspection Reading', "reading_10", "label", "Sample 10", "Data")

def execute():
   property_setter() 