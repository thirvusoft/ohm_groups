import frappe

from datetime import datetime

def checkin(doc, actions):
    date_time_obj = datetime.strptime(doc.time, '%Y-%m-%d %H:%M:%S')

    date_str = date_time_obj.date().strftime('%d-%m-%Y')
    time_str = date_time_obj.time().strftime('%H:%M:%S')
    doc.attendance_date = date_str
    doc.attendance_time = time_str
