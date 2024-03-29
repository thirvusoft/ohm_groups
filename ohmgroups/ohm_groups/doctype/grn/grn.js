// Copyright (c) 2023, thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('GRN', {
	refresh: function(frm) {

        frm.set_query("party_type",function(){
            return {
                filters:{
                    "name":["in",["Customer","Supplier"]]
                },
            }
        }),
        frm.set_query("items","items",function(){
            return {
                filters:{
                    "has_variants":0
                }
                
            }
        })
		frm.set_query("transporter", function() {
			return {
				filters: {
					is_transporter: 1
				}
			};
		});
		if(!frm.doc.branch){
            frm.call({
                
                method: "grn_address_company",
                args:{
                    company:frm.doc.company,
                },
    
                callback: function(r) {
                    frm.set_value("company_address",r.message)
            }
            })
        }
	},
    mode_of_transport(frm) {
        frm.set_value("gst_vehicle_type", get_vehicle_type(frm.doc));
    },
    // branch(frm) {
    //     frm.call({
            
    //         method: "grn_branch_address_company",
    //         args:{
    //             company:frm.doc.company,
    //             branch:frm.doc.branch,
    //         },
    //         callback: function(r) {
    //                 cur_frm.set_value("company_address",r.message)
                
    //     }
    //     })
    // },
    
    party: function(frm){
        frm.set_value("party_name",frm.doc.party)
        frm.call({
            
            method: "grn_on_insert",
            args:{
                party:frm.doc.party,
            },
            callback: function(r) {
                    cur_frm.set_value("warehouse",r.message)
                
        }
        }),
                      
        frm.call({
            
            method: "grn_address_shipping",
            args:{
                party_type:frm.doc.party_type,
                party : frm.doc.party,
            },

            callback: function(r) {
                frm.set_value("shipping_address_name",r.message)
        }
        }),
        frm.call({
            
            method: "grn_address_billing",
            args:{
                party_type:frm.doc.party_type,
                party : frm.doc.party,
            },

            callback: function(r) {
                frm.set_value("customer_address",r.message)
        }
        })
    
    },
    trigger: function(frm,cdt,cdn){
	
        var data = locals[cdt][cdn]
        frm.call({
            method: "grn_dc_items",
            args : {
                items : data.items,
                party : frm.doc.party,
                party_type : frm.doc.party_type,
                company: frm.doc.company,
                purchase_order:frm.doc.purchase_order

            },
            callback: function(r){
				if(r.message[1]){
					frappe.msgprint(r.message[1]);
				}
                else if(frm.doc.purchase_order){
                    frm.set_value("dc_items",r.message[2])
                }
				else{
					frm.set_value("dc_items",r.message[0])
				// 	for(let i=0;i<r.message[0].length;i++){
               	// 	   var row = frm.add_child("dc_items")
                // 	   row["item_code"] = r.message[0][i].item_code
                // 	   row["dc_no"] = r.message[0][i].dc_no
                // 	   row["total_qty_in_dc"] = r.message[0][i].total_qty_in_dc
                // 	   row["qty"] = r.message[0][i].qty
                // 	   row["dc_name"] = r.message[0][i].dc_name
                // 	   row["balanced_qty"] = r.message[0][i].balanced_qty
                   
                // }
                frm.refresh_fields("dc_items")
				}
				

			
                
                
            }
        })
    },
    quality_inspection:function(frm,cdt,cdn){
        frm.set_value("qc",1)
        var data = locals[cdt][cdn]
        frm.call({
            freeze:true,
            freeze_message:"Quality Inspection Creating....",
            method: "create_inspection",
            args: {
                items : frm.doc.items,
                name : frm.doc.name,
                gate_entry : frm.doc.gate_entry,
                party_type : frm.doc.party_type,
                party : frm.doc.party,
                received_doc_no : frm.doc.received_doc_no
            },
            callback: function(r){
                frappe.db.set_value("GRN",frm.doc.name,"qc",1).then(()=>{
                    frm.reload_doc()
                    if (frm.doc.qc == 1) {
                        var owner = frm.doc.owner;
                        var doctype = frm.doctype;
                        var name = frm.doc.name;
                        frm.call({
                            method: "qc_check",
                            args: {
                                qc: frm.doc.qc,
                                doctype: doctype,
                                name: name,
                                owner: owner
                            },
                            callback: function(r) {
                                if (!r.exc) {
                                    // show success message
                                    frappe.show_alert({
                                        message: __("Quality Inspection Created"),
                                        indicator: 'green'
                                    });
                                }
                            }
                        });
                    }
                })
                
                
            }
        })
        
        }
        
    
});
frappe.ui.form.on("DC Received Items",{
	qty: function(frm,cdt,cdn){
		var row = locals[cdt][cdn]
		frappe.model.set_value(cdt,cdn,"balanced_qty",(parseFloat(row.total_qty_in_dc) -parseFloat(row.qty)))
	}
})
frappe.ui.form.on("GRN Items",{
	items:function(frm,cdt,cdn){
		var row = locals[cdt][cdn]
		frappe.model.set_value(cdt,cdn,"item_code",(row.items))     
	}
})

function get_vehicle_type(doc) {
    if (doc.mode_of_transport == "Road") return "Regular";
    if (doc.mode_of_transport == "Ship") return "Over Dimensional Cargo (ODC)";
    return "";
}

