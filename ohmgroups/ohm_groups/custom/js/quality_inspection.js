var template
frappe.ui.form.on('Quality Inspection', {
		refresh: function(frm, cdt, cdn) {
			cur_frm.fields_dict["readings"].$wrapper.find('.grid-body .rows').find(".grid-row").each(function(i, item) {
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
		},
		is_parameter :function(frm, cdt, cdn) {
				cur_frm.set_value("readings",[])
				

		},

		quality_inspection_template: function(frm){
			template = frm.doc.quality_inspection_template
		},
		onload: function(frm){
			template = frm.doc.quality_inspection_template

		}
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