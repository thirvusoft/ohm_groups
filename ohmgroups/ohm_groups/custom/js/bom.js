frappe.ui.form.on('BOM',{
    with_operations:function(frm,cdt,cdn){
        var row = locals[cdt][cdn]
        frappe.call({
            
            method: "ohmgroups.ohm_groups.custom.py.bom.operations_",
            args:{
                item:frm.doc.item,
            },

            callback: function(r) {
                frm.set_value("item",r.message[0])
                frm.set_value("operations",r.message[1])
                
                // frm.set_value("operations",r.message[0])
                  
        }
        })
    }
})