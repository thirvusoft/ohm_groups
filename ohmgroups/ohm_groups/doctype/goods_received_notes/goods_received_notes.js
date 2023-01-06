// Copyright (c) 2023, thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Goods Received Notes', {
	refresh: function(frm) {
        frm.set_query("party_type",function(){
            return {
                filters:{
                    "name":["in",["Customer","Supplier"]]
                }
                
            }
        }),
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

});
frappe.ui.form.on('GRN Items',{
    items: function(frm,cdt,cdn){
        var data = locals[cdt][cdn]
        frm.call({
            method: "grn_dc_items",
            args : {
                items : data.items,
                party : frm.doc.party,
                party_type : frm.doc.party_type,
                company: frm.doc.company
            },
            callback: function(r){
                for(let i=0;i<r.message.length;i++){
                   var row = frm.add_child("dc_items")
                   row["item_code"] = r.message[i].item_code
                   row["dc_no"] = r.message[i].dc_no
                   row["qty"] = r.message[i].qty
                   
                }
                frm.refresh_field("dc_items")
                
            }
        })
    }
})
function get_vehicle_type(doc) {
    if (doc.mode_of_transport == "Road") return "Regular";
    if (doc.mode_of_transport == "Ship") return "Over Dimensional Cargo (ODC)";
    return "";
}
