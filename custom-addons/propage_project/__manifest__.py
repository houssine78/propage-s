# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Propage-s Custom Project Module",
    "version": "17.0.1.0.2",
    "category": "Project",
    "author": "Open Architects Consulting",
    "website": "https://www.openarchitecsconsulting.com",
    "license": "AGPL-3",
    "depends": [
        "propage_base",
        "project",
        "calendar",
        "hr_timesheet",
        "hr_timesheet_sheet",
        "web_widget_x2many_2d_matrix"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/propage_project_data.xml",
        "report/timesheet_analysis_report_views.xml",
        "views/calendar_views.xml",
        "views/task_views.xml",
        "views/hr_timesheet_sheet_views.xml",
        "views/meeting_type_views.xml",
        "views/partner_views.xml",
        "wizard/calendar_time_registration_view.xml",
    ],
    "installable": True,
}
