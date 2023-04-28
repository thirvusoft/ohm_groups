from datetime import datetime
import frappe
from datetime import timedelta

from frappe import _
from frappe.utils import cint, get_datetime, get_link_to_form

@frappe.whitelist()
def add_log_based_on_employee_field(
    employee_field_value,
	timestamp,
	device_id=None,
	log_type=None,
	skip_auto_attendance=0,
	employee_fieldname="attendance_device_id",
):
    
    if not employee_field_value or not timestamp:
        frappe.throw(_("'employee_field_value' and 'timestamp' are required."))

    employee = frappe.db.get_values(
		"Employee",
		{employee_fieldname: employee_field_value},
		["name", "employee_name", employee_fieldname],
		as_dict=True,
	)
    if employee:
        employee = employee[0]
    else:
        frappe.throw(
			_("No Employee found for the given employee field value. '{}': {}").format(
				employee_fieldname, employee_field_value
			)
		)
# Given timestamp in string
    date_format_str = '%Y-%m-%d %H:%M:%S'
    validate_timestamp = datetime.strptime(str(timestamp), date_format_str)
    resetting_checkin_time = frappe.db.get_single_value("Thirvu HR Settings", "checkin_type_resetting_time")
    resetting_checkin_time=datetime.strptime(str(resetting_checkin_time),'%H:%M:%S')
    resetting_datetime = datetime.combine(validate_timestamp.date() if(validate_timestamp.time() > resetting_checkin_time.time()) else (validate_timestamp.date() + timedelta(days = -1)), resetting_checkin_time.time())

        #TS Code Start
    try:
        att_doc = frappe.get_last_doc("Employee Checkin", {"employee": employee.name,"time": [">", str(resetting_datetime)]})

        # create datetime object from timestamp string
        given_time = datetime.strptime(str(att_doc.time), date_format_str)


        # Buffer Time
        buffer_time = frappe.db.get_single_value("Thirvu HR Settings", "buffer_time")
        frappe.log_error(title="test", message = buffer_time)

        # Add 2 minutes to datetime object
        final_time = given_time + timedelta(minutes=buffer_time)
        frappe.log_error(title="testing", message = final_time)

        # Convert datetime object to string in specific format
        final_time_str = final_time.strftime('%Y-%m-%d %H:%M:%S')
        # frappe.log_error(title="te1", message = final_time_str)
        # frappe.log_error(title="te2", message = timestamp)

        if final_time_str < timestamp:
            doc = frappe.new_doc("Employee Checkin")
            doc.employee = employee.name
            doc.employee_name = employee.employee_name
            doc.time = timestamp
            doc.device_id = device_id
            if(att_doc.log_type=="IN"):
                doc.log_type = "OUT"
            else:
                doc.log_type="IN"
            if cint(skip_auto_attendance) == 1:
                doc.skip_auto_attendance = "1"
            doc.insert()
            return doc
        else:
            return att_doc
    except :
        doc = frappe.new_doc("Employee Checkin")
        doc.employee = employee.name
        doc.employee_name = employee.employee_name
        doc.time = timestamp
        doc.device_id = device_id
        doc.log_type = 'IN'
        if cint(skip_auto_attendance) == 1:
            doc.skip_auto_attendance = "1"
        doc.insert()
        return doc
    

    #TS Code End