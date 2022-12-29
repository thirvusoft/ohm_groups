import frappe

def time_count(doc,actions):
    time  = frappe.get_all("Employee Checkin",{"employee":doc.name,"designation":"Helper"},pluck="time",order_by="time")
    b=0
    for i in range(0,len(time), 2):
        a= time[i+1] - time[i]
        minutes = a.total_seconds() / 60
        # hrs = minutes/60
        b = b+minutes
    doc.total_count_ = round(b/60)

