# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Propage-s Custom CRM Module",
    "version": "17.0.1.0.0",
    "category": "CRM",
    "author": "Open Architects Consulting",
    "website": "https://www.openarchitecsconsulting.com",
    "license": "AGPL-3",
    "depends": [
        "crm",
        "propage_base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/crm_stage_data.xml",
        "views/crm_lead.xml"
    ],
    "installable": True,
}
