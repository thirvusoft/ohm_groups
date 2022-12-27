from erpnext.stock.doctype.quality_inspection.quality_inspection import QualityInspection
import frappe

def validate(doc,actions):
    for i in doc.readings:
        for j in range(1, 11):
            reading = "reading_" + str(j)
            if i.get(reading):
                if(doc.sample_size < j):
                    frappe.throw("Quantity is greater than "+i.specification)
                    
def status(doc, actions):
    for j in range(1, 11):
        for i in doc.readings:
            data = doc.get_formula_evaluation_data(i)
            reading = "reading_" + str(j)
            condition = i.acceptance_formula
            data["mean"] = sum([float(m.get(reading) or 0)  for m in doc.readings]) / len(doc.readings)
            data["min_value"] = sum([float(m.get("min_value") or 0)  for m in doc.readings]) / len(doc.readings)
            data["max_value"] = sum([float(m.get("max_value") or 0)  for m in doc.readings]) / len(doc.readings)
            if(data["mean"] == 0):
                continue
            try:
                result = frappe.safe_eval(condition, None, data)
                doc.update({ 
                    "sample_" + str(j) : "Accepted" if result else "Rejected",
                    })
            except Exception:
                frappe.throw(
                    frappe._("Row #{0}: Acceptance Criteria Formula is incorrect.").format(reading.idx),
                    title=frappe._("Invalid Formula"),
                )

class quality_inspection(QualityInspection):
    
	@frappe.whitelist()
	def get_item_specification_details(self):
		if not self.quality_inspection_template:
			self.quality_inspection_template = frappe.db.get_value(
				"Item", self.item_code, "quality_inspection_template"
			)

		if not self.quality_inspection_template:
			return

		self.set("readings", [])
		parameters = get_template_details(self.quality_inspection_template)
		for d in parameters:
			child = self.append("readings", {})
			child.update(d)
			child.status = "Accepted"


def get_template_details(template):
	if not template:
		return []

	return frappe.get_all(
		"Item Quality Inspection Parameter",
		fields=[
			"specification",
			"value",
			"acceptance_formula",
			"numeric",
			"formula_based_criteria",
			"min_value",
			"max_value",
			"testing_type",
		],
		filters={"parenttype": "Quality Inspection Template", "parent": template},
		order_by="idx",
	)

import json

@frappe.whitelist()
def add_attachment(file, name):
	if(isinstance(file, str)):
		file = json.loads(file)
	file = frappe.get_doc('File', file)
	file.update({
		'name':'',
		'attached_to_name': name,
		'attached_to_doctype': 'Quality Inspection',
		'attached_to_field' : 'balloon_drawing'
	})
	file.insert()
