# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Propage-s Entrepreneur Case",
    "version": "16.0.1.0.0",
    "category": "CRM",
    "author": "Open Architects Consulting",
    "website": "https://www.openarchitecsconsulting.com",
    "license": "AGPL-3",
    "depends": [
        "base",
        "project",
        "propage_base",
        "propage_crm",
        "propage_project"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/create_task_from_template.xml",
        "views/entrepreneur_case.xml",
        "views/entrepreneur_team.xml",
        "views/partner.xml",
        "views/entrepreneur_case_menu.xml",
        "views/crm_lead.xml",
    ],
    "installable": True,
}
