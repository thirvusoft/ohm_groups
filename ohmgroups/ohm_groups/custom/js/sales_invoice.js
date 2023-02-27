frappe.ui.form.on('Sales Invoice',{
    customer_name:function(frm){
        frappe.db.get_value('Customer',{'name':frm.doc.customer_name},'_default_item',(r)=>{
            if(r._default_item == 1){
                frappe.call({
                    method: "ohmgroups.ohm_groups.custom.py.sales_invoice.item_customers",
                    args:{
                        customer_name:frm.doc.customer_name,
                    },
                    callback: function(r) {
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
    }


})


