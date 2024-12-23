app_name = "biometric"
app_title = "Biometric"
app_publisher = "8848 Digital"
app_description = "biometric"
app_email = "shyamkumar@8848digital.cm"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "biometric",
# 		"logo": "/assets/biometric/logo.png",
# 		"title": "Biometric",
# 		"route": "/biometric",
# 		"has_permission": "biometric.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/biometric/css/biometric.css"
# app_include_js = "/assets/biometric/js/biometric.js"

# include js, css files in header of web template
# web_include_css = "/assets/biometric/css/biometric.css"
# web_include_js = "/assets/biometric/js/biometric.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "biometric/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "biometric/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "biometric.utils.jinja_methods",
# 	"filters": "biometric.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "biometric.install.before_install"
# after_install = "biometric.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "biometric.uninstall.before_uninstall"
# after_uninstall = "biometric.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "biometric.utils.before_app_install"
# after_app_install = "biometric.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "biometric.utils.before_app_uninstall"
# after_app_uninstall = "biometric.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "biometric.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
# Explicitly import the method for testing purposes

# scheduler_events = {
#     "cron": {
#         "*/10 * * * *": ["biometric.biometric.doctype.attendance_biometric.attendance_biometric.create_employee_checkin"]
#     }
# }
# /home/ascra/Documents/biomatric-8848/frappe-bench/apps/biometric/biometric/biometric/doctype/attendance_biometric/attendance_biometric.py

# frappe-bench/apps/biometric/biometric/biometric/doctype/attendance_biometric/attendance_biometric.py
# frappe-bench/apps/biometric/biometric/biometric/doctype/attendance_biometric/attendance_biometric.py

# /home/ascra/Documents/biomatric-8848/frappe-bench/apps/biometric/biometric/biometric/api/essl/fetch_attendance.py


# frappe-bench/apps/biometric/biometric/biometric/api/essl/fetch_attendance.py

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"biometric.tasks.all"
# 	],
# 	"daily": [
# 		"biometric.tasks.daily"
# 	],
# 	"hourly": [
# 		"biometric.tasks.hourly"
# 	],
# 	"weekly": [
# 		"biometric.tasks.weekly"
# 	],
# 	"monthly": [
# 		"biometric.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "biometric.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "biometric.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "biometric.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["biometric.utils.before_request"]
# after_request = ["biometric.utils.after_request"]

# Job Events
# ----------
# before_job = ["biometric.utils.before_job"]
# after_job = ["biometric.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"biometric.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


# scheduler_events = {
#     "cron": {
#         "*/10 * * * *": ["biometric.biometric.doctype.attendance_biometric.attendance_biometric.validate"]
#     }
# }

# apps/biometric/biometric/biometric/api/essl/fetch_attendance.py
# biometric.biometric.api.essl.fetch_attendance.get_attendance_logs

scheduler_events = {
    "cron": {
        "*/10 * * * *": [
            "biometric.biometric.api.essl.fetch_attendance.get_attendance_logs"
        ]
    }
}

