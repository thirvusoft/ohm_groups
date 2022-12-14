frappe.ui.form.on("Purchase Order", {
    
    is_subcontracted: function(frm){
        frappe.call({
            
            method: "ohmgroups.ohm_groups.custom.py.purchase_order.on_insert",
            args:{
                supplier:frm.doc.supplier,
                is_subcontracted:frm.doc.is_subcontracted
            },
            callback: function(r) {
                if(frm.doc.is_subcontracted){
                    cur_frm.set_value("supplier_warehouse",r.message)
                }
        }
        })
    },
    supplier: function(frm){
        if(frm.doc.supplier){
        frappe.call({
            method: "ohmgroups.ohm_groups.custom.py.purchase_order.item_supplier",
            args:{
                supplier:frm.doc.supplier,
            },
            callback: function(r) {
                if(frm.doc.supplier!= ""){
                    var count =0
                    frm.set_value('items',[]);
                    r.message.forEach(element => {
                        var row = cur_frm.add_child('items')
                        frappe.model.set_value(row.doctype,row.name,'item_code',element.item_code)
                    });
                           
                } 
        }
        })}
        else{
            var count =0
            frm.set_value('items',[]);
        }
    },
})

