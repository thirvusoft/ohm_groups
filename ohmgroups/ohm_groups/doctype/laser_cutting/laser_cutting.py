# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from collections import defaultdict
from frappe import scrub
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.utils import nowdate, unique
import erpnext
from erpnext.stock.get_item_details import _get_item_tax_template


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def item_query(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
	filters = {}
	doctype = "Item"
	conditions = []

	if isinstance(filters, str):
		filters = json.loads(filters)

	# Get searchfields from meta and use in Item Link field query
	meta = frappe.get_meta(doctype, cached=True)
	searchfields = meta.get_search_fields()

	columns = ""
	extra_searchfields = [field for field in searchfields if not field in ["name", "description"]]

	if extra_searchfields:
		columns += ", " + ", ".join(extra_searchfields)

	if "description" in searchfields:
		columns += """, if(length(tabItem.description) > 40, \
			concat(substr(tabItem.description, 1, 40), "..."), description) as description"""

	searchfields = searchfields + [
		field
		for field in [searchfield or "name", "item_code", "item_group", "item_name"]
		if not field in searchfields
	]
	searchfields = " or ".join([f"tabItem.{field}" + " like %(txt)s" for field in searchfields])

	if filters and isinstance(filters, dict):
		if filters.get("customer") or filters.get("supplier"):
			party = filters.get("customer") or filters.get("supplier")
			item_rules_list = frappe.get_all(
				"Party Specific Item", filters={"party": party}, fields=["restrict_based_on", "based_on_value"]
			)

			filters_dict = {}
			for rule in item_rules_list:
				if rule["restrict_based_on"] == "Item":
					rule["restrict_based_on"] = "name"
				filters_dict[rule.restrict_based_on] = []

			for rule in item_rules_list:
				filters_dict[rule.restrict_based_on].append(rule.based_on_value)

			for filter in filters_dict:
				filters[scrub(filter)] = ["in", filters_dict[filter]]

			if filters.get("customer"):
				del filters["customer"]
			else:
				del filters["supplier"]
		else:
			filters.pop("customer", None)
			filters.pop("supplier", None)

	description_cond = ""
	if frappe.db.count(doctype, cache=True) < 50000:
		# scan description only if items are less than 50000
		description_cond = "or tabItem.description LIKE %(txt)s"

	return frappe.db.sql(
		"""select
			tabItem.name {columns}
		from tabItem 
		left join `tabItem Variant Attribute` iv ON iv.parent = tabItem.name
		where tabItem.docstatus < 2
            and iv.attribute_value = "Laser Cutting"
			and tabItem.disabled=0
			and tabItem.has_variants=0
			and (tabItem.end_of_life > %(today)s or ifnull(tabItem.end_of_life, '0000-00-00')='0000-00-00')
			and ({scond} or tabItem.item_code IN (select parent from `tabItem Barcode` where barcode LIKE %(txt)s)
				{description_cond})
			{fcond} {mcond}
		
		order by
			if(locate(%(_txt)s, tabItem.name), locate(%(_txt)s, tabItem.name), 99999),
			if(locate(%(_txt)s, tabItem.item_name), locate(%(_txt)s, tabItem.item_name), 99999),
			
			tabItem.name, tabItem.item_name
		limit %(start)s, %(page_len)s """.format(
			columns=columns,
			scond=searchfields,
			fcond=get_filters_cond(doctype, filters, conditions).replace("%", "%%"),
			mcond=get_match_cond(doctype).replace("%", "%%"),
			description_cond=description_cond,
		),
		{
			"today": nowdate(),
			"txt": "%%%s%%" % txt,
			"_txt": txt.replace("%", ""),
			"start": start,
			"page_len": page_len,
		},
		as_dict=as_dict,
	)


class LaserCutting(Document):
    def on_submit(self):
        document = frappe.new_doc("Stock Entry")
        document.stock_entry_type ="Repack"
        document.laser_cutting = self.name
        for m in self.laser_cutting:
            item = frappe.get_doc("Item",{"name":m.item_code})
            for j in item.uoms:
                if item.stock_uom == j.uom:
                    document.append('items', dict(
                        item_code = m.item_code,
                        qty=m.qty,
                        s_warehouse = m.warehouse,
                        basic_rate= m.basic_rate_as_per_stock_uom,
                        stock_uom = item.stock_uom,
                        uom= m.uom,

                    ))
        for i in self.raw_materials:
            item = frappe.get_doc("Item",{"name":i.item_code})
            
            for j in item.uoms:
                if item.stock_uom == j.uom:
                    document.append('items', dict(
                        item_code = i.item_code,
                        qty=i.qty,
                        t_warehouse = i.warehouse,
                        basic_rate=i.basic_rate_as_per_stock_uom,
                        stock_uom = item.stock_uom,
                        uom=i.uom,

                    ))
        document.save(ignore_permissions=True)
        document.submit()

    def on_cancel(self):
        if frappe.db.exists("Stock Entry",{"laser_cutting":self.name}):
            frappe.get_doc("Stock Entry",{"laser_cutting":self.name}).cancel()
    def on_trash(self):
        if frappe.db.exists("Stock Entry",{"laser_cutting":self.name}):
            frappe.get_doc("Stock Entry",{"laser_cutting":self.name}).delete()
