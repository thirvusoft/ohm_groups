# Copyright (c) 2023, thirvusoft and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe.model.document import Document
import json
from collections import defaultdict
from frappe import scrub
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.utils import nowdate, unique
import erpnext
from erpnext.stock.get_item_details import _get_item_tax_template
from frappe.utils.data import get_datetime, time_diff_in_seconds


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

@frappe.whitelist()
def make_time_log(args):
    if isinstance(args, str):
        args = json.loads(args)
    args = frappe._dict(args)
    doc = frappe.get_doc("Laser Cutting", args.job_card_id)
    # doc.validate_sequence_id()
    doc.add_time_logs(args)
    
# @frappe.whitelist()
# def make_tot_completed_qty(time_logs):
#     log = json.loads(time_logs)

#     tot = 0
#     for i in log:
#         tot+=i.get('completed_qty')
#     return tot

@frappe.whitelist()
def sheet_no(laser_cutting):
    sheet_number = ['\n']
    raw_item = json.loads(laser_cutting)
    for i in range(1, int(raw_item[0].get('qty'))+1, 1):
        name ="Sheet" + str(i)
        sheet_number.append([name])
    return sheet_number

@frappe.whitelist()
def set_time_log(number_of_sheets,designation,operators,designation_2,helpers):
    time_log_add = []
    now = datetime.now()
    ope = json.loads(operators)
    help = json.loads(helpers)
    for i in ope:
        time_log_add.append({'sheet_no':number_of_sheets,'operators_name':designation,'employee':i.get('employee'),'from_time':now})
    for j in help:
        time_log_add.append({'sheet_no':number_of_sheets,'helpers_name':designation_2,'employee':j.get('employee_id_'),'from_time':now})
    return time_log_add


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
    
    def add_time_logs(self, args):
        from datetime import timedelta

        last_row = []
        employees = args.employees
        if isinstance(employees, str):
            employees = json.loads(employees)

        if self.time_logs and len(self.time_logs) > 0:
            last_row = self.time_logs[-1]

        self.reset_timer_value(args)
        # emp = {i.employee:"Operators" for i in self.operators}
        # emp.update({i.employee_id_:"Helpers" for i in self.helpers})
        if last_row and args.get("complete_time"):
            for row in self.time_logs:
                if not row.get('to_time'):
                    employee = row.get('employee')
                    curr_last_time = get_datetime(args.get("complete_time"))
                    time = args['data'].get("time0").split(":")
                    row.update(
                        {
                            "to_time": curr_last_time + timedelta(hours = int(time[0]),minutes=int(time[1]),seconds=int(time[2])),
                            "operation": args.get("sub_operation"),
                            "completed_qty": args['data'].get("qty0") or 0.0,
                            "item_code":args['data'].get("item0") or ""
                        }
                    )
                    for i in range(1, len(self.raw_materials)):
                        curr_last_time += timedelta(seconds=1)
                        time = args['data'].get(f"time{i}").split(":")
                        frappe.errprint(self.total_qty)
                    
                        self.append("time_logs",
                            {
                            "employee":employee,
                            "from_time":curr_last_time,
                            "operation": args.get("sub_operation"),
                            "to_time": curr_last_time + timedelta(hours = int(time[0]),minutes=int(time[1]),seconds=int(time[2])),
                            "completed_qty": args['data'].get(f"qty{i}") or 0.0,
                            "item_code":args['data'].get(f"item{i}") or "",
                            
                        }
                        )
                        curr_last_time += timedelta(hours = int(time[0]),minutes=int(time[1]),seconds=int(time[2]))
                        self.employee = []
                    # row.update(
                    #     {
                    #         "to_time": get_datetime(args.get("complete_time")),
                    #         "operation": args.get("sub_operation"),
                    #         "completed_qty": args.get("completed_qty") or 0.0,
                    #     }
                    # )
        elif args.get("start_time"):
            new_args = frappe._dict(
                {
                    "from_time": get_datetime(args.get("start_time")),
                    "operation": args.get("sub_operation"),
                    "completed_qty": 0.0,
                }
            )
            if employees:
                for name in employees:
                    new_args.employee = name.get("employee")
                    new_args.operators_name=frappe.get_value('Employee',name.get("employee"),'designation')
                    # new_args.operators_name=args.get('help')
                    new_args.sheet_no=args.get('sheet')
                    self.add_start_time_log(new_args)
            else:
                self.add_start_time_log(new_args)

        if not self.employee and employees:
            self.set_employees(employees)

        if self.status == "On Hold":
            self.current_time = time_diff_in_seconds(last_row.to_time, last_row.from_time)
        tot = 0
        
        for i in self.time_logs:
            tot+=i.get('completed_qty')
            self.total_completed_qty = tot
            # i.sheet_no = self.number_of_sheets
            # i.operators_name = self.designation
            # i.operators_name = self.designation_2
        # frappe.db.set_value("Laser Cutting",self.name,"number_of_sheets","")
        # frappe.db.set_value("Laser Cutting",self.name,"number_of_sheets","")
        self.save()
    def add_start_time_log(self, args):
        self.append("time_logs", args)

    def set_employees(self, employees):
        for name in employees:
            self.append("employee", {"employee": name.get("employee"), "completed_qty": 0.0})

    def reset_timer_value(self, args):
        self.started_time = None

        if args.get("status") in ["Work In Progress", "Complete"]:
            self.current_time = 0.0

            if args.get("status") == "Work In Progress":
                self.started_time = get_datetime(args.get("start_time"))

        if args.get("status") == "Resume Job":
            args["status"] = "Work In Progress"

        if args.get("status"):
            self.status = args.get("status")
        
    def update_sub_operation_status(self):
        if not (self.sub_operations and self.time_logs):
            return

        operation_wise_completed_time = {}
        for time_log in self.time_logs:
            if time_log.operation not in operation_wise_completed_time:
                operation_wise_completed_time.setdefault(
                    time_log.operation,
                    frappe._dict(
                        {"status": "Pending", "completed_qty": 0.0, "completed_time": 0.0, "employee": []}
                    ),
                )

            op_row = operation_wise_completed_time[time_log.operation]
            op_row.status = "Work In Progress" if not time_log.time_in_mins else "Complete"
            if self.status == "On Hold":
                op_row.status = "Pause"

            op_row.employee.append(time_log.employee)
            if time_log.time_in_mins:
                op_row.completed_time += time_log.time_in_mins
                op_row.completed_qty += time_log.completed_qty

        for row in self.sub_operations:
            operation_deatils = operation_wise_completed_time.get(row.sub_operation)
            if operation_deatils:
                if row.status != "Complete":
                    row.status = operation_deatils.status

                row.completed_time = operation_deatils.completed_time
                if operation_deatils.employee:
                    row.completed_time = row.completed_time / len(set(operation_deatils.employee))

                    if operation_deatils.completed_qty:
                        row.completed_qty = operation_deatils.completed_qty / len(set(operation_deatils.employee))
            else:
                row.status = "Pending"
                row.completed_time = 0.0
                row.completed_qty = 0.0
    def validate(self):
        tot_qty = 0
        for i in self.raw_materials:
            tot_qty += int(i.total_qty)
            self.total_qty = tot_qty
        if len(self.time_logs) == 0:
            self.status = "Draft"
            self.total_completed_qty = 0
            self.employee = []
        tot = 0
        for i in self.time_logs:
            tot+=i.get('completed_qty')
            self.total_completed_qty = tot