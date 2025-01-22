from odoo import fields, models


class MassMailingList(models.Model):
    _inherit = "mailing.list"

    newsletter_traced_action = fields.Boolean(
        string="Sync contact from newsletter action result"
    )
    mass_mailing_id = fields.Many2one(
        'mailing.mailing',
        string="Newsletter",
        help="Select the newsletter from which you want to generate the contact based on the result"
    )
    traced_action = fields.Selection([
        ('open', 'Opened'),
        ('not_open', 'Not opened'),
        ('reply', 'Replied'),
        ('open_no_click', 'Opened but no click'),
        ('open_and_click', 'Opened and clicked'),
        ],
        default="open",
        string="Action to track"
    )

    def _action_get_partner_filtered(self):
        massmailing = self.mass_mailing_id
        if self.traced_action == 'reply':
            found_traces = massmailing.mailing_trace_ids.filtered(lambda trace: trace.trace_status == 'reply')
        elif self.traced_action == 'delivered':
            found_traces = massmailing.mailing_trace_ids.filtered(lambda trace: trace.trace_status == 'sent')
        elif self.traced_action == 'open':
            found_traces = massmailing.mailing_trace_ids.filtered(
                lambda trace: trace.trace_status in ('open', 'reply')
            )
        elif self.traced_action == 'open_no_click':
            found_traces = massmailing.mailing_trace_ids.filtered(
                lambda trace: trace.trace_status == 'open' and not trace.links_click_datetime
            )
        elif self.traced_action == 'open_and_click':
            found_traces = massmailing.mailing_trace_ids.filtered(
                lambda trace: trace.trace_status in ('open', 'reply') and trace.links_click_datetime
            )
        else:
            found_traces = self.env['mailing.trace']
        partner_ids = found_traces.mapped('partner_id')
        
        return partner_ids

    def action_sync(self):
        """Sync contacts in dynamic lists."""
        Contact = self.env["mailing.contact"].with_context(syncing=True)
        Partner = self.env["res.partner"]
        # Skip non-dynamic lists
        dynamic = self.filtered("dynamic").with_context(syncing=True)
        for one in dynamic:
            desired_partners = None
            if self.newsletter_traced_action:
                desired_partners = self._action_get_partner_filtered()
            else:
                sync_domain = [("email", "!=", False)] + safe_eval(one.sync_domain)
                desired_partners = Partner.search(sync_domain)
            # Detach or remove undesired contacts when synchronization is full
            if one.sync_method == "full":
                contact_to_detach = one.contact_ids.filtered(
                    lambda r: r.partner_id not in desired_partners
                )
                one.contact_ids -= contact_to_detach
                contact_to_detach.filtered(lambda r: not r.list_ids).unlink()
            # Add new contacts
            current_partners = one.contact_ids.mapped("partner_id")
            contact_to_list = self.env["mailing.contact"]
            vals_list = []
            for partner in desired_partners - current_partners:
                contacts_in_partner = partner.mass_mailing_contact_ids
                if contacts_in_partner:
                    contact_to_list |= contacts_in_partner[0]
                else:
                    vals_list.append(
                        {"list_ids": [(4, one.id)], "partner_id": partner.id}
                    )
            one.contact_ids |= contact_to_list
            Contact.create(vals_list)
            one.is_synced = True
        # Invalidate cached contact count
        dynamic.invalidate_recordset(["contact_count"])
