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
    naming_supplier: function(frm){
        cur_frm.set_value("supplier",frm.doc.naming_supplier)
        if(frm.doc.supplier){
            frappe.db.get_value('Supplier',{'name':frm.doc.supplier},'default_item',(r)=>{
                if(r.default_item == 1){
                    frappe.call({
                        method: "ohmgroups.ohm_groups.custom.py.purchase_order.item_supplier",
                        args:{
                            supplier:frm.doc.supplier,
                        },
                        callback: function(r) {
                            frm.set_query("item_code","items",function(){
                                return {
                                    filters:{
                                        "item_code":["in",r.message]
                                    }
                                    
                                }
                            })
                    }
                    })
                
                }
            })
        }
        else{
            var count =0
            frm.set_value('items',[]);
        }
        
    },
    
    
})

