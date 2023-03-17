var party_items = []

function itemFilters(frm) {
    if (!frm.doc.naming_supplier) {
        party_items = []
        return
    }
    frappe.db.get_value('Supplier', { 'name': frm.doc.naming_supplier }, 'default_item', (r) => {
        if (r.default_item == 1) {
            frappe.call({
                method: "ohmgroups.ohm_groups.custom.py.purchase_order.item_supplier",
                args: {
                    naming_supplier: frm.doc.naming_supplier,
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
        itemFilters(frm)
    },
    refresh: function(frm,cdt,cdn){
        itemFilters(frm)
        // frm.set_query("item_code","items",function(){
        //     return {
        //         filters:{
        //             "item_group":"Services"
        //         }
                
        //     }
        // })
        frm.add_custom_button(__('Subcontracted Receipt'), function(){
            var so_no = frappe.db.get_list('Subcontracting Order', {filters:{'purchase_order':frm.doc.name, 'docstatus':1},fields:['name']}).then((r)=>{
                if(!r.length){
                    frappe.throw("Create Subcontracting Order...")
                }
                frappe.call({
                    method: 'erpnext.subcontracting.doctype.subcontracting_order.subcontracting_order.make_subcontracting_receipt',
                    args: {
                        source_name:r[0].name,},
                        callback: function(r) {
                            if(r.message) {
                                frappe.model.sync(r.message)
                                frappe.set_route("Form", r.message.doctype,r.message.name);
                                return;
                            }
                        }

                });
                
            })

        }, __("Create"));
        // frm.add_custom_button(__('Material to Transfer'), function(){
        //     var so = frappe.db.get_list('Subcontracting Order', {filters:{'purchase_order':frm.doc.name, 'docstatus':1},fields:['name']}).then((so_name)=>{
        //         if(so_name.length){
        //         frappe.call({
        //             method: 'erpnext.controllers.subcontracting_controller.make_rm_stock_entry',
        //             args: {
        //                 subcontract_order: so_name[0].name,
        //                 order_doctype: "Subcontracting Order"
        //             },
        //             callback: (r) => {
        //                 var doclist = frappe.model.sync(r.message);
        //                 frappe.set_route('Form', doclist[0].doctype, doclist[0].name);
        //             }
        //         });
        //     }
        //         })
        // }, __("Transfer"));

            
        
        
    },

    
})

frappe.ui.form.on('Purchase Order Item', {
	// stock_uom_rate:function(frm,cdt,cdn) {
        
	// 	var row = locals[cdt][cdn]
    //     frappe.model.set_value(cdt,cdn,'rate',row.stock_uom_rate)
	// 	frappe.model.set_value(cdt,cdn,'amount',row.stock_uom_rate * row.stock_qty)
	// },
	
	weight_per_unit:function(frm,cdt,cdn) {
        
		var row = locals[cdt][cdn]
        frappe.model.set_value(cdt,cdn,'total_weight',row.weight_per_unit * row.qty)

	},
	total_weight:function(frm,cdt,cdn) {
        
		var row = locals[cdt][cdn]
        frappe.model.set_value(cdt,cdn,'weight_per_unit',row.total_weight / row.qty)

	},
    item_code: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn]
        if (row.item_code && !frm.doc.party) {
            frappe.model.set_value(cdt, cdn, "item_name", "")
            frappe.model.set_value(cdt, cdn, "item_code", "")
            frappe.throw("Kindly fill Supplier")

        }
        if (row.item_code && !party_items.includes(row.item_code)) {
            let item_code = row.item_code
            frappe.model.set_value(cdt, cdn, "item_name", "")
            frappe.model.set_value(cdt, cdn, "item_code", "")
            frappe.throw(`<b>${item_code}</b> does not belong to <b>${frm.doc.naming_supplier}</b>`)

        }
    }
})
// function po_item (frm,cdt,cdn){
//     var row = locals[cdt][cdn]
//     frappe.model.set_value(cdt,cdn,'rate',row.stock_uom_rate)
//     frappe.model.set_value(cdt,cdn,'amount',row.stock_uom_rate * row.stock_qty) 
// }		