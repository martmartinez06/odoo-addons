import base64
import io
from odoo import models, fields, api

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False


class AccountMove(models.Model):
    _inherit = 'account.move'

    qr_code_image = fields.Binary(
        string='QR Code',
        compute='_compute_qr_code',
        store=False,
        help='QR code containing invoice payment information'
    )
    show_qr_on_invoice = fields.Boolean(
        string='Show QR on Invoice',
        default=True,
        help='Display QR code on printed invoice'
    )

    @api.depends('name', 'amount_total', 'invoice_date_due', 'partner_id', 'company_id', 'state')
    def _compute_qr_code(self):
        for move in self:
            if not QRCODE_AVAILABLE:
                move.qr_code_image = False
                continue
                
            if move.move_type in ('out_invoice', 'out_refund') and move.state == 'posted':
                qr_data = move._build_qr_data()
                
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_data)
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                move.qr_code_image = base64.b64encode(buffer.getvalue())
            else:
                move.qr_code_image = False

    def _build_qr_data(self):
        """
        Build QR data string.
        Override this method for custom formats (e.g., EPC QR for SEPA).
        
        Returns:
            str: Data to encode in QR code
        """
        self.ensure_one()
        data_parts = [
            f"INV:{self.name or ''}",
            f"AMT:{self.amount_total:.2f}",
            f"CUR:{self.currency_id.name or 'EUR'}",
        ]
        
        if self.invoice_date_due:
            data_parts.append(f"DUE:{self.invoice_date_due.strftime('%Y-%m-%d')}")
        
        if self.company_id.vat:
            data_parts.append(f"VAT:{self.company_id.vat}")
        
        if self.partner_id.name:
            partner_name = self.partner_id.name[:30]
            data_parts.append(f"TO:{partner_name}")
        
        if self.ref:
            data_parts.append(f"REF:{self.ref[:20]}")
        
        return '|'.join(data_parts)

    def action_regenerate_qr_code(self):
        """Manual QR regeneration button action"""
        self._compute_qr_code()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'QR Code',
                'message': 'QR code has been regenerated.',
                'type': 'success',
                'sticky': False,
            }
        }
