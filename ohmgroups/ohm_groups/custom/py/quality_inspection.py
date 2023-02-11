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

@frappe.whitelist()                
def status(doc, actions = None):
    res={}
    if isinstance(doc, str):
        doc=frappe.get_doc(json.loads(doc))
    for j in range(1, 11):
        res["sample_" + str(j)]=""
        for i in doc.readings:
            data = doc.get_formula_evaluation_data(i)
            reading = "reading_" + str(j)
            condition = i.acceptance_formula
            try:
                mean_readings = [float(m.get(reading) or 0)  for m in doc.readings if (m.get(reading) or "").lower()!="ok"]
                data["mean"] = sum(mean_readings) / len(mean_readings)
                min_value_readings =[float(m.get("min_value") or 0)  for m in doc.readings if (m.get(reading) or "").lower()!="ok"]
                data["min_value"] = sum(min_value_readings) / len(min_value_readings)
                max_readings = [float(m.get("max_value") or 0)  for m in doc.readings if (m.get(reading) or "").lower()!="ok"]
                data["max_value"] = sum(max_readings) / len(max_readings)
            except ValueError as e:
                frappe.throw("Sample reading must be an number or 'OK'")
            except BaseException:
                frappe.errprint(frappe.get_traceback())
                frappe.throw("Couldn't Get Results") 
            if(data["mean"] == 0):
                continue
            try:
            
                result = frappe.safe_eval(condition, None, data)
                doc.update({ 
                    "sample_" + str(j) : "Accepted" if result or doc.get("sample_" + str(j)) == "Accepted" else "Rejected",
                    })
                if result == False:
                    res["sample_" + str(j)]="Rejected"
                    # break
                else:
                    res["sample_" + str(j)]="Accepted"
            except Exception:
                frappe.throw(
                    frappe._("Row #{0}: Acceptance Criteria Formula is incorrect.").format(reading.idx),
                    title=frappe._("Invalid Formula"),
                )
    return res

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

class OhmQualityInspection(QualityInspection):
    
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
    def update_qc_reference(self):
        quality_inspection = self.name if self.docstatus == 1 else ""

        if self.reference_type == "Job Card":
            if self.reference_name:
                frappe.db.sql(
                    """
                    UPDATE `tab{doctype}`
                    SET quality_inspection = %s, modified = %s
                    WHERE name = %s and production_item = %s
                """.format(
                        doctype=self.reference_type
                    ),
                    (quality_inspection, self.modified, self.reference_name, self.item_code),
                )

        else:
            args = [quality_inspection, self.modified, self.reference_name, self.item_code]
            if self.reference_type != "GRN":
                doctype = self.reference_type + " Item"
            else:
                doctype = self.reference_type + " Items"

            if self.reference_type == "Stock Entry":
                doctype = "Stock Entry Detail"

            if self.reference_type and self.reference_name:
                conditions = ""
                if self.batch_no and self.docstatus == 1:
                    conditions += " and t1.batch_no = %s"
                    args.append(self.batch_no)

                if self.docstatus == 2:  # if cancel, then remove qi link wherever same name
                    conditions += " and t1.quality_inspection = %s"
                    args.append(self.name)

                frappe.db.sql(
                    """
                    UPDATE
                        `tab{child_doc}` t1, `tab{parent_doc}` t2
                    SET
                        t1.quality_inspection = %s, t2.modified = %s
                    WHERE
                        t1.parent = %s
                        and t1.item_code = %s
                        and t1.parent = t2.name
                        {conditions}
                """.format(
                        parent_doc=self.reference_type, child_doc=doctype, conditions=conditions
                    ),
                    args,
                )


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
            "tolerance_level"
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

def inspection_status(doc,actions):
        inspection = frappe.get_doc("GRN", {'name':doc.grn})
        for i in inspection.quality_inspection_doc_no:
            if doc.name == i.quality_inspection_doc_no:
                if i.inspection_list == 0:
                        if doc.docstatus == 1:
                            i.inspection_list = 1
        inspection.save()