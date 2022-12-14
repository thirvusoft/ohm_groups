frappe.ui.form.on("Purchase Order Item", {
    
    fg_item_qty: function(frm,cdt,cdn){
        const row = locals[cdt][cdn]
        frappe.call({
            
            method: "ohmgroups.ohm_groups.custom.py.purchase_order.uom_qty",
            args:{
                items:frm.doc.items,
                is_subcontracted : frm.doc.is_subcontracted
            },

            callback: function(r) {
                
                frappe.model.set_value(cdt,cdn,"qty",row.fg_item_qty*r.message)
                frappe.model.set_value(cdt,cdn,"fg_item_qty",row.fg_item_qty)
                  
        }
        })
    },
  
})

