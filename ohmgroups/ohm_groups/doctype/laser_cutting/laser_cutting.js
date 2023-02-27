// Copyright (c) 2023, thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laser Cutting', {
    refresh:function(frm){
        frm.fields_dict.laser_cutting.$wrapper[0].addEventListener("click",function(){
            if(frm.doc.laser_cutting.length == 1){
                frm.fields_dict.laser_cutting.$wrapper.find('.grid-add-row')[0].style.display='none'
            }
        })
        if(frm.doc.laser_cutting.length == 1){
            frm.fields_dict.laser_cutting.$wrapper.find('.grid-add-row')[0].style.display='none'
        }
        
       

		frm.set_query("item_code","raw_materials", function() {
			return {
				query: "ohmgroups.ohm_groups.doctype.laser_cutting.laser_cutting.item_query",
				filters: {
					"attribute_value": "Laser Cutting",
				}
			};
		});
		frm.set_query("item_code","laser_cutting", function() {
			return {
                filters: {
                    item_group: "Sheet",

                  },
			};
		});
    },
    // setup:function(frm){
    //         cur_frm.fields_dict.laser_cutting.$wrapper.find('.grid-add-row')[0].style.display='none'
    // },
    validate:async function (frm){
        if(!frm.doc.raw_materials ){
            frappe.msgprint("Kindly Upload the Raw Materials")
        }
        else if(frm.doc.raw_materials == 0){
            frappe.msgprint("Kindly Upload the Raw Materials")
        }
        else{
            for(var i=0;i<frm.doc.raw_materials.length;i++){
                var rate = (await frappe.db.get_value('Item',{'item_code':frm.doc.raw_materials[i].item_code},'valuation_rate')).message.valuation_rate
                    frappe.model.set_value(frm.doc.raw_materials[i].doctype,frm.doc.raw_materials[i].name,'basic_rate_as_per_stock_uom',rate)
                    frappe.model.set_value(frm.doc.raw_materials[i].doctype,frm.doc.raw_materials[i].name,'warehouse',"Stores - ONE")
                
            }
frm.refresh()
        }


},
});

frappe.ui.form.on('Raw Materials',{
    item_code(frm,cdt,cdn) {
        var row = locals[cdt][cdn]
        frappe.db.get_value('Item',{'item_code':row.item_code},'valuation_rate').then((r)=>{
            frappe.model.set_value(cdt,cdn,'basic_rate_as_per_stock_uom',r.message.valuation_rate)
        })
	},

})

