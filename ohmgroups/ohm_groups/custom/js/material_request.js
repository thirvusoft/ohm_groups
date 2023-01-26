frappe.ui.form.on("Material Request",{
    make_custom_buttons: function(frm){
        if (frm.doc.material_request_type === "Purchase" && frm.doc.docstatus == 1 && frm.doc.status != 'Stopped') {
            frm.add_custom_button(__('Purchase Receipt'),
                () => frm.events.make_purchase_receipt(frm), __('Create'));
        } 
    },

	make_purchase_receipt: function(frm) {
		frappe.prompt(
			{
				label: __('For Default Supplier (Optional)'),
				fieldname:'default_supplier',
				fieldtype: 'Link',
				options: 'Supplier',
				description: __('Select a Supplier from the Default Suppliers of the items below. On selection, a Purchase Order will be made against items belonging to the selected Supplier only.'),
				get_query: () => {
					return{
						query: "erpnext.stock.doctype.material_request.material_request.get_default_supplier_query",
						filters: {'doc': frm.doc.name}
					}
				}
			},
			(values) => {
				frappe.model.open_mapped_doc({
					method: "ohmgroups.ohm_groups.custom.py.material_request.make_purchase_receipt",
					frm: frm,
					args: { default_supplier: values.default_supplier },
					run_link_triggers: true
				});
			},
			__('Enter Supplier'),
			__('Create')
		)
	},


})
