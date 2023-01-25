frappe.ui.form.on("Material Request",{
    refresh: function(frm){
        if (frm.doc.material_request_type === "Purchase" && frm.doc.docstatus == 1 && frm.doc.status != 'Stopped') {
            frm.add_custom_button(__('Purchase Receipt'),
                () => frm.events.make_purchase_receipt(frm), __('Create'));
        } 
    }
})