// Copyright (c) 2022, thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Gate Entry', {
	refresh: function(frm) {
		frm.set_query("party_type",function(){
            return {
                filters:{
                    "name":["in",["Purchase Order","DC Not for Sales","Supplier"]]
                }
                
            }
        })
		frm.set_query("purchase_order",function(){
            return {
                filters:{
                    "docstatus":1
                }
                
            }
        })
		frm.set_query("dc_not_for_sales",function(){
            return {
                filters:{
                    "docstatus":1
                }
                
            }
        })

	},
    against_party: function(frm,cdt,cdn){
	
        var data = locals[cdt][cdn]
        frm.call({
            method: "get_items",
            args : {
				party_type : frm.doc.party_type,
                dc_not_for_sales : frm.doc.dc_not_for_sales,
                purchase_order : frm.doc.purchase_order
				
            },
            callback: function(r){
				if(r.message[1] == "Error Message"){
					frappe.msgprint(r.message[0]);
				}
				else{
					// frm.set_value("items",r.message[frm.doc.party_type == "DC Not for Sales"?0:1])
                    if(!r.message.length){
                        frappe.msgprint(" All the Qty are received");
                    }
                    else{
                        frm.set_value("items",r.message)
                    }
                    
					
				}
				}
 
            
        })
    }
});
frappe.ui.form.on('Gate Entry Item', {
	received_qty: function(frm,cdt,cdn) {
		var row = locals[cdt][cdn]
		frappe.model.set_value(cdt,cdn,'balanced_qty',row.qty - row.received_qty)
	}
})