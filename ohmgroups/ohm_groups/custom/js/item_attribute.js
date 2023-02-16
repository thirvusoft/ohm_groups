// frappe.ui.form.on("Item Attribute Value",{
//     before_item_attribute_values_remove:function (frm,doctype, name) {
//         var row = frappe.get_doc(doctype, name);
//         console.log(row.attribute_value)
//         frappe.call({
//             method:"ohmgroups.ohm_groups.custom.py.item_attribute.delete_item",
//             args:{item_name:row.attribute_value},

//         }) 
//     }
// })