# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from odoo import models, fields


class POSSession(models.Model):
    _inherit = "pos.session"

    stop_at = fields.Datetime(
        readonly=False,
    )

    def write(self, vals):
        if vals.get('stop_at') and self._context.get('custom_action_session_close'):
            for rec in self:
                if rec.stop_at:
                    vals.pop('stop_at')
        return super(POSSession, self).write(vals)

    def action_pos_session_closing_control(self):
        res = super(POSSession, self.with_context(custom_action_session_close=True)).action_pos_session_closing_control()
        return res

    def _create_account_move(self):
        timezone_tz = 'utc'
        user_id = self.env.user
        if user_id.tz:
            timezone_tz = user_id.tz
        local = pytz.timezone(timezone_tz)
        local_dt = local.utcoffset(self.stop_at)
        custom_pos_session_close_at = (self.stop_at + local_dt).date() #CONVERT UTC TIME TO USER TIMEZONE
#        res = super(POSSession, self.with_context(custom_pos_session_close_at=self.stop_at.date()))._create_account_move()
        res = super(POSSession, self.with_context(custom_pos_session_close_at=custom_pos_session_close_at))._create_account_move()
        return res
