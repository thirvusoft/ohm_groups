frappe.ui.form.on("Stock Entry" ,{
    refresh:function(frm){
        frm.add_custom_button(__('Purchase Order'), function(){
            frappe.route_options = {
                "naming_supplier": frm.doc.suppliername,
                "dc_no": frm.doc.name
            };
            frappe.set_route("Form", "Purchase Order","new_doc.name");
        

        }, __("Create"));
    },
    suppliername: function(frm){
        cur_frm.set_value("supplier",frm.doc.suppliername)
        frappe.call({
            
            method: "ohmgroups.ohm_groups.custom.py.stock_entry.on_insert",
            args:{
                supplier:frm.doc.suppliername,
            },
            callback: function(r) {
                    cur_frm.set_value("to_warehouse",r.message)
                    cur_frm.set_value("from_warehouse","Stores - ONE")
            
        }
        })
    },

});