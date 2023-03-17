// Copyright (c) 2022, thirvusoft and contributors
// For license information, please see license.txt

var party_items = []

function itemFilters(frm) {
    if (!frm.doc.party_name || !frm.doc.party_type) {
        party_items = []
        return
    }
    frappe.db.get_value('Supplier', { 'name': frm.doc.party_name }, 'default_item', (r) => {
        if (r.default_item == 1) {
            frm.call({
                method: "item_supplier",
                args: {
                    party_name: frm.doc.party_name,
                },
                callback: function (r) {
                    party_items = r.message || []
                    frm.set_query("item_code", "items", function () {
                        return {
                            filters: {
                                "item_code": ["in", r.message]
                            }

                        }
                    })
                }
            })

        }

    })
    frappe.db.get_value('Customer', { 'name': frm.doc.party_name }, '_default_item', (r) => {
        if (r._default_item == 1) {
            frm.call({
                method: "item_customer",
                args: {
                    party_name: frm.doc.party_name,
                },
                callback: function (r) {
                    party_items = r.message || []
                    frm.set_query("item_code", "items", function () {
                        return {
                            filters: {
                                "item_code": ["in", r.message]
                            }

                        }
                    })
                }
            })

        }

    })
}



frappe.ui.form.on('Gate Entry', {
	refresh: function(frm) {
        itemFilters(frm)
		frm.set_query("party_type",function(){
            return {
                filters:{
                    "name":["in",["Supplier","Customer"]]
                }
                
            }
        })
        


	},
    party_name : function(frm){





        itemFilters(frm)
		frm.set_query("purchase_order",function(){
            return {
                filters:{
                    "docstatus":1,
                    "naming_supplier": frm.doc.party_name
                }
                
            }
        })

		frm.set_query("dc_not_for_sales",function(){
            return {
                filters:{
                    "docstatus":1,
                    "party_name": frm.doc.party_name
                }
                
            }
        })
		frm.set_query("sales_invoice",function(){
            return {
                filters:{
                    "docstatus":1,
                    "customer": frm.doc.party_name
                }
                
            }
        })
    },

    is_gate_entry_in__out : function(frm){
        if(frm.doc.is_gate_entry_in__out == "IN"){
            frm.set_query("party_type",function(){
                return {
                    filters:{
                        "name":["in",["Supplier","Customer"]]
                    }
                    
                }
            })
        }
        else if(frm.doc.is_gate_entry_in__out == "OUT"){
            frm.set_query("party_type",function(){
                return {
                    filters:{
                        "name":["in",["Supplier","Customer"]]
                    }
                    
                }
            })
        }
        else{
            frm.set_query("party_type",function(){
                return {
                    filters:{
                        "name":["in",["Purchase Order","DC Not for Sales","Supplier"]]
                    }
                    
                }
            })
        }

    },
    against_party: function(frm,cdt,cdn){
	
        var data = locals[cdt][cdn]
        frm.call({
            method: "get_items",
            args : {
				party_type : frm.doc.party_type,
                dc_not_for_sales : frm.doc.dc_not_for_sales,
                purchase_order : frm.doc.purchase_order,
                against_po__dc : frm.doc.against_po__dc,
                party_name : frm.doc.party_name,
                against_si__dc : frm.doc.against_si__dc,
                sales_invoice : frm.doc.sales_invoice,
                is_gate_entry_in__out : frm.doc.is_gate_entry_in__out
				
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
	},
    item_code: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        if (row.item_code && !frm.doc.party_name) {
            frappe.model.set_value(cdt, cdn, "item_name", "")
            frappe.model.set_value(cdt, cdn, "item_code", "")
            frappe.throw("Kindly fill party")

        }
        if (row.item_code && !party_items.includes(row.item_code)) {
            let item_code = row.item_code
            frappe.model.set_value(cdt, cdn, "item_name", "")
            frappe.model.set_value(cdt, cdn, "item_code", "")
            frappe.throw(`<b>${item_code}</b> does not belong to ${frm.doc.party_type} <b>${frm.doc.party_name}</b>`)

        }
    }
})