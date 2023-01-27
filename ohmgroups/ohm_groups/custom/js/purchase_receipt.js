frappe.ui.form.on("Purchase Receipt",{

	refresh: function(frm) {
        if (frm.doc.docstatus == 0) {
            frm.add_custom_button(__('Material Request'),
                function () {
                    erpnext.utils.map_current_doc({
                        method: "ohmgroups.ohm_groups.custom.py.purchase_receipt.material_request_item",
                        source_doctype: "Material Request",
                        target: me.frm,
                        setters: {
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
        frm.add_custom_button(__('Stop'),
        // () => frm.events.update_status(frm, 'Stopped'));
	// },
    
    
})
