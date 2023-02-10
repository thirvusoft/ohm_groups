frappe.ui.form.on("Purchase Receipt",{

	refresh: function(frm) {
        if (frm.doc.docstatus == 0) {
            
            frm.add_custom_button(__('Material Request'),
                function () {
                    if (!me.frm.doc.supplier) {
                        frappe.throw({
                            title: __("Mandatory"),
                            message: __("Please Select a Supplier")
                        });
                    }
                    erpnext.utils.map_current_doc({
                        method: "ohmgroups.ohm_groups.custom.py.purchase_receipt.material_request_item",
                        source_doctype: "Material Request",
                        target: me.frm,
                        setters: {
                            supplier_name_: me.frm.doc.supplier,
                            schedule_date: undefined
                        },
                        get_query_filters: {
                            docstatus: 1,
                            per_received: ["<", 99.99],
                            company: me.frm.doc.company
                        }
                    })
                }, __("Get Items From"));
        }
        if (frm.doc.docstatus == 0) {
            
            frm.add_custom_button(__('Gate Entry'),
                function () {
                    erpnext.utils.map_current_doc({
                        method: "ohmgroups.ohm_groups.doctype.gate_entry.gate_entry.gate_entry_item",
                        source_doctype: "Gate Entry",
                        target: me.frm,
                        setters:{},
                        get_query_filters: {
                            docstatus: 1,
                        }
                    })
                }, __("Get Items From"));
        }
        
	},

    
})
