frappe.ui.form.on("Job Card", {
    onload: function(frm){
        if(frm.doc.check_time == 0){
        frm.set_value('time_logs',[])
        frm.set_value('check_time',1)
        frm.refresh()
        }}
})