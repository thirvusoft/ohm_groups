# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

# @frappe.whitelist()
# def goods_items(company,items):
#     rec_items = frappe.get_all("DC Not for Sales",{'company':company,""},pluck="party_name")
#     print('Mani')
#     return rec_items
        


class GoodsReceivedNotes(Document):
    pass
