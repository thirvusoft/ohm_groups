var template
var called=0;
frappe.ui.form.on('Quality Inspection', {
		refresh: function(frm, cdt, cdn) {
			frm.set_query("party_type_",function(){
				return {
					filters:{
						"name":["in",["Customer","Supplier"]]
					}
					
				}
			})
			if(frm.doc.quality_inspection_template){
				frm.doc.item_code?frappe.db.get_doc("Quality Inspection Template", frm.doc.quality_inspection_template).then(( itemimage ) => {
						frm.set_value("balloon_drawing",document.location.origin + itemimage.item_image.replace(/ /g, "%20"))
					
						
					// cur_frm.fields_dict.balloon_drawing.refresh()
					// <img class="img-responsive" src="${itemimage.image}" onerror="cur_frm.toggle_display('preview', false)" />
					// </div>`);
				
				}):null;
			}

			cur_frm.fields_dict["readings"]?.$wrapper.find('.grid-body .rows')?.find(".grid-row")?.each(function(i, item) {
	            let d = locals[cur_frm.fields_dict["readings"].grid.doctype][$(item).attr('data-name')];
				if(d['min_value'] > d['reading_1'] || d['reading_1'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_1"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_2'] || d['reading_2'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_2"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_3'] || d['reading_3'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_3"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_4'] || d['reading_4'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_4"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_5'] || d['reading_5'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_5"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_6'] || d['reading_6'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_6"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_7'] || d['reading_7'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_7"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_8'] || d['reading_8'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_8"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_9'] || d['reading_9'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_9"]').css({'color': 'red'});
				}
				if(d['min_value'] > d['reading_10'] || d['reading_10'] > d['max_value']){
					$(item).find('.grid-static-col[data-fieldname="reading_10"]').css({'color': 'red'});
				}
            });
			if(frm.doc.quality_inspection_template){
			frappe.db.get_doc("Quality Inspection Template", frm.doc.quality_inspection_template).then(( image ) => {
				frm.get_field("image")?.$wrapper.html(`<div class="img_preview">
				<img class="img-responsive" src="${image.item_image}" onerror="cur_frm.toggle_display('preview', false)" />
				</div>`);
			});		
				
			}
		},
		quality_inspection_template: function(frm){
			if(frm.doc.quality_inspection_template){
				frm.doc.item_code?frappe.db.get_doc("Quality Inspection Template", frm.doc.quality_inspection_template).then(( itemimage ) => {
						frm.set_value("balloon_drawing",document.location.origin + itemimage.item_image.replace(/ /g, "%20"))
						frm.refresh(quality_inspection_template)
						
					// cur_frm.fields_dict.balloon_drawing.refresh()
					// <img class="img-responsive" src="${itemimage.image}" onerror="cur_frm.toggle_display('preview', false)" />
					// </div>`);
				
				}):null;
			}
		},
		item_code : function(frm){
			frappe.db.get_doc("Item", frm.doc.item_code).then(( itemimage ) => {
				frm.get_field("item_image")?.$wrapper.html(`<div class="img_preview">
				<img class="img-responsive" src="${itemimage.image}" onerror="cur_frm.toggle_display('preview', false)" />
				</div>`);
				if(frm.doc.quality_inspection_template){
				frm.doc.item_code?frappe.db.get_doc("Quality Inspection Template", frm.doc.quality_inspection_template).then(( itemimage ) => {
					frm.set_value("balloon_drawing",document.location.origin + itemimage.item_image.replace(/ /g, "%20"))
				
					
				// cur_frm.fields_dict.balloon_drawing.refresh()
				// <img class="img-responsive" src="${itemimage.image}" onerror="cur_frm.toggle_display('preview', false)" />
				// </div>`);
			
			}):null;
		}	
			});
		},
		get_result:  function(frm) {
			 frappe.call({
				method: "ohmgroups.ohm_groups.custom.py.quality_inspection.status",
				args: {
					doc: cur_frm.doc
				},
				callback: function(r) {
					Object.keys(r.message)?.forEach(key => {
						frm.set_value(key, r.message[key])
					})
				}
			})
		},
		is_parameter :function(frm, cdt, cdn) {
				cur_frm.set_value("readings",[])
				cur_frm.set_value("sample_1","")
				cur_frm.set_value("sample_2","")
				cur_frm.set_value("sample_3","")
				cur_frm.set_value("sample_4","")
				cur_frm.set_value("sample_5","")
				cur_frm.set_value("sample_6","")
				cur_frm.set_value("sample_7","")
				cur_frm.set_value("sample_8","")
				cur_frm.set_value("sample_9","")
				cur_frm.set_value("sample_10","")

		},

		after_save: async function(frm){
			if(called>0)return
			called+=1
			template = frm.doc.quality_inspection_template
			if(frm.doc.quality_inspection_template){
				(await frappe.db.get_list("File", {
					filters: {
						"attached_to_doctype":"Quality Inspection Template",
						"attached_to_name": cur_frm.doc.quality_inspection_template,
						
					},
					fields: ["name", "is_private", "file_url", "file_name"]
				}))?.forEach(att => {
					frappe.call({
						method:'ohmgroups.ohm_groups.custom.py.quality_inspection.add_attachment',
						args:{
							file:att,
							name:frm.doc.name,
						},
						freeze:true,
						async:false,
						freeze_message:'Attaching documents.....',
						callback(){
							frm.refresh()

						}
					})
					
				});
			}
		},
		before_save: function(frm){
			frm.doc.item_code?frappe.db.get_doc("Item", frm.doc.item_code).then(( itemimage ) => {
				frm.get_field("item_image").$wrapper.html(`<div class="img_preview">
				<img class="img-responsive" src="${itemimage.image}" onerror="cur_frm.toggle_display('preview', false)" />
				</div>`);
			}):null;

		},
		onload: function(frm){
			template = frm.doc.quality_inspection_template

		},
   });

frappe.ui.form.on("Quality Inspection Reading",{
	si_no: function(frm,cdt,cdn){
		frappe.db.get_doc("Quality Inspection Template", template)
				.then((doc) => {
					for(var i=0;i<doc.item_quality_inspection_parameter.length;i++){
						var row = locals[cdt][cdn]
						if(row.si_no == doc.item_quality_inspection_parameter[i].si_no ){
							frappe.model.set_value(cdt,cdn,"specification",doc.item_quality_inspection_parameter[i].specification)
							frappe.model.set_value(cdt,cdn,"min_value",doc.item_quality_inspection_parameter[i].min_value)
							frappe.model.set_value(cdt,cdn,"max_value",doc.item_quality_inspection_parameter[i].max_value)
							frappe.model.set_value(cdt,cdn,"formula_based_criteria",doc.item_quality_inspection_parameter[i].formula_based_criteria)
							frappe.model.set_value(cdt,cdn,"acceptance_formula",doc.item_quality_inspection_parameter[i].acceptance_formula)
						}
						
					}
				});
	}
})