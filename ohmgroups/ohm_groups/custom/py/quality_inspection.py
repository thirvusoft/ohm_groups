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
                    "sample_" + str(j): "Accepted" if result else "Rejected",
                    })
            except Exception:
                frappe.throw(
                    frappe._("Row #{0}: Acceptance Criteria Formula is incorrect.").format(reading.idx),
                    title=frappe._("Invalid Formula"),
                )

                
                