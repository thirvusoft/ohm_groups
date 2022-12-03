console.log("value[0].maximum_value")
frappe.ui.form.on("Quality Inspection",{
    refresh: function(frm){
        for(let i=0;i<frm.doc.readings.length;i++){
            console.log("value[0].maximum_value")
            var row = locals[frm.doc.readings[i].doctype][frm.doc.readings[i].name]
            var value = frappe.get_list("Item Quality Inspection Parameter",{'parent':frm.doc.quality_inspection_template,'specification':row.specification}, ['maximum_value','minimmum_value'])
            console.log(value)
            console.log("value[0].maximum_value")
            frappe.model.set_value(frm.doc.readings[i].doctype,frm.doc.readings[i].name,'maximum_value',value.maximum_value);
            frappe.model.set_value(frm.doc.readings[i].doctype,frm.doc.readings[i].name,'minimum_value',value.minimmum_value);

        }

    }
})