// frappe.ui.form.on("Delivery Note", {
    
//     supplier: function(frm){
//         frappe.call({
            
//             method: "ohmgroups.ohm_groups.custom.py.delivery_note.on_insert",
//             args:{
//                 supplier:frm.doc.supplier,
//                 is_subcontracted:frm.doc.is_subcontracted
//             },
//             callback: function(r) {
//                 if(frm.doc.is_subcontracted){
//                     cur_frm.set_value("supplier_warehouse",r.message)
//                 }
//         }
//         })
//     },

// })