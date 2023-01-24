// Copyright (c) 2023, thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Laser Cutting', {
    trigger:async function (frm){

        for(var i=0;i<frm.doc.raw_materials.length;i++){
            var rate = (await frappe.db.get_value('Item',{'item_code':frm.doc.raw_materials[i].item_code},'valuation_rate')).message.valuation_rate
                frappe.model.set_value(frm.doc.raw_materials[i].doctype,frm.doc.raw_materials[i].name,'basic_rate_as_per_stock_uom',rate)
            
        }
frm.refresh()
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

