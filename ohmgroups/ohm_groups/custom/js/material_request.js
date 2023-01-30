frappe.ui.form.on("Material Request",{
    refresh: function(frm){

			if (frm.doc.material_request_type === "Purchase") {
				frm.add_custom_button(__('Purchase Receipt'),
					() => frm.events.make_purchase_receipt(frm), __('Create'));
			}
		
    },
    supplier_name_: function(frm){
            frappe.db.get_value('Supplier',{'name':frm.doc.supplier_name_},'default_item',(r)=>{
                if(r.default_item == 1){
                    frappe.call({
                        method: "ohmgroups.ohm_groups.custom.py.material_request.item_supplier",
                        args:{
                            supplier:frm.doc.supplier_name_,
                        },
                        callback: function(r) {
							console.log("dd")
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
