frappe.ui.form.on('BOM',{
    with_operations:function(frm,cdt,cdn){
        var row = locals[cdt][cdn]
        if(!frm.doc.item){
            frappe.throw("Kindly fill the item")
        }
        frappe.call({
            
            method: "ohmgroups.ohm_groups.custom.py.bom.operations_",
            args:{
                item:frm.doc.item,
            },

            callback: function(r) {
                
                frm.set_value("item",r.message[0])
                frm.set_value("operations",r.message[1])
                frm.set_query("operation","items", function () {
                    return {
                      filters: {
                        name: ["in",r.message[2]],

                      },
                    };
                  });
                // frm.set_value("operations",r.message[0])
                  
        }
        })
        // for(let i=0;i<frm.doc.operations.length;i++){
        //     list.push(frm.doc.operations[i].operation)
        //     console.log(frm.doc.operations[i].operation)
        // }
    },
    // refresh: function(frm,cdt,cdn){
    //     var row = locals[cdt][cdn]

    // }
})
