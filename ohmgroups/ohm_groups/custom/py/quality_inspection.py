from itertools import count
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
    if(doc.quality_inspection_template):
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

def count_status(doc, actions):
    doc.accepted_1 = 0
    doc.rejected_1 = 0
    if doc.sample_1 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_1 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1
    if doc.sample_2 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_2 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1
    if doc.sample_3 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_3 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1
    if doc.sample_4 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_4 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1
    if doc.sample_5 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_5 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1
    if doc.sample_6 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_6 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1
    if doc.sample_7 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_7 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1        
    if doc.sample_8 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_8 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1        
    if doc.sample_9 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_9 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1
    if doc.sample_10 == "Accepted":
        doc.accepted_1 = doc.accepted_1 +1
    elif doc.sample_10 == "Rejected":
        doc.rejected_1 = doc.rejected_1+1
    else:
        doc.accepted_1 = doc.accepted_1 
        doc.rejected_1 = doc.rejected_1

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
            "testing_type"
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
