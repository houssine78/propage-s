# Copyright 2023 Open Architects Consulting SRL (https://www.openarchitecsconsulting.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Propage-s Base Module",
    "version": "16.0.1.0.0",
    "category": "CRM",
    "author": "Open Architects Consulting",
    "website": "https://www.openarchitecsconsulting.com",
    "license": "AGPL-3",
    "depends": [
        "propage_community_base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/propage_base_security.xml",
        "views/propage_base_menu.xml"
    ],
    "installable": True,
}
