# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Propage-s Custom Project Module",
    "version": "16.0.1.0.0",
    "category": "Project",
    "author": "Open Architects Consulting",
    "website": "https://www.openarchitecsconsulting.com",
    "license": "AGPL-3",
    "depends": [
        "propage_base",
        "project",
        "hr_timesheet",
        "hr_timesheet_sheet"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/propage_project_data.xml",
        "views/task_views.xml",
        "views/hr_timesheet_sheet_views.xml"
    ],
    "installable": True,
}
