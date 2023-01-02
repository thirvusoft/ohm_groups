from . import __version__ as app_version

app_name = "ohmgroups"
app_title = "Ohm Groups"
app_publisher = "thirvusoft"
app_description = "Wind Mill"
app_email = "thirvusoft@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ohmgroups/css/ohmgroups.css"
# app_include_js = "/assets/ohmgroups/js/ohmgroups.js"

# include js, css files in header of web template
# web_include_css = "/assets/ohmgroups/css/ohmgroups.css"
# web_include_js = "/assets/ohmgroups/js/ohmgroups.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ohmgroups/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "ohmgroups.utils.jinja_methods",
#	"filters": "ohmgroups.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ohmgroups.install.before_install"
after_install = "ohmgroups.install.after_install"
after_migrate = "ohmgroups.install.after_install"


# Uninstallation
# ------------

# before_uninstall = "ohmgroups.uninstall.before_uninstall"
# after_uninstall = "ohmgroups.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ohmgroups.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Quality Inspection": "ohmgroups.ohm_groups.custom.py.quality_inspection.quality_inspection"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

doc_events = {
    "Quality Inspection" : {
        
        "validate": [
            "ohmgroups.ohm_groups.custom.py.quality_inspection.validate",
                     "ohmgroups.ohm_groups.custom.py.quality_inspection.status",]
                     },
	"Vehicle Log":{
		"on_update_after_submit": "ohmgroups.ohm_groups.custom.py.vehicle_log.onsubmit",
		"on_submit": ["ohmgroups.ohm_groups.custom.py.vehicle_log.onsubmit",
						"ohmgroups.ohm_groups.custom.py.vehicle_log.onsubmit_hours",
						"ohmgroups.ohm_groups.custom.py.vehicle_log.update_transport_cost",
						"ohmgroups.ohm_groups.custom.py.vehicle_log.vehicle_log_draft",
						"ohmgroups.ohm_groups.custom.py.vehicle_log.vehicle_log_mileage",
		],
		"on_cancel" :["ohmgroups.ohm_groups.custom.py.vehicle_log.onsubmit",
						"ohmgroups.ohm_groups.custom.py.vehicle_log.update_transport_cost"
			],
		"validate" :["ohmgroups.ohm_groups.custom.py.vehicle_log.validate",
						"ohmgroups.ohm_groups.custom.py.vehicle_log.validate_distance",
						"ohmgroups.ohm_groups.custom.py.vehicle_log.total_cost"

		]

	},
	"Driver" :{
		"validate" : "ohmgroups.ohm_groups.custom.py.driver.validate_phone"
	},
	"Purchase Order" : {
		"on_submit" : "ohmgroups.ohm_groups.custom.py.purchase_order.po_order"
	},
	# "Subcontracting Order" : {
	# 	"on_submit" : "ohmgroups.ohm_groups.custom.py.subcontracting_order.validate"
	# },
	"Quality Inspection Template" : {
		"validate" : "ohmgroups.ohm_groups.custom.py.quality_insprection_template.item_template"
	},
	"Item Attribute" : {
		"validate" : "ohmgroups.ohm_groups.custom.py.item_attribute.attribute_item"
	},
	"Employee" : {
		"validate": "ohmgroups.ohm_groups.custom.py.employee.time_count"
	}
}
doctype_js = {
    "Quality Inspection" : "/ohm_groups/custom/js/quality_inspection.js",
    "Purchase Order" :[ "/ohm_groups/custom/js/purchase_order.js",
                       "/ohm_groups/custom/js/purchase_order_items.js"],
    "Vehicle" : "/ohm_groups/custom/js/vehicle.js",
    "Vehicle Log" : ["/ohm_groups/custom/js/vehicle_log.js",
                     "/ohm_groups/custom/js/vehicle_log_service.js"],
    "Item Attribute" :"/ohm_groups/custom/js/item_attribute.js",
    "Employee" : "/ohm_groups/custom/js/employee.js",
    "Stock Entry" : "/ohm_groups/custom/js/stock_entry.js"
                      
 
    
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"ohmgroups.tasks.all"
#	],
#	"daily": [
#		"ohmgroups.tasks.daily"
#	],
#	"hourly": [
#		"ohmgroups.tasks.hourly"
#	],
#	"weekly": [
#		"ohmgroups.tasks.weekly"
#	],
#	"monthly": [
#		"ohmgroups.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "ohmgroups.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "ohmgroups.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "ohmgroups.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"ohmgroups.auth.validate"
# ]
