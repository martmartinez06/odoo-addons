{
    'name': 'Invoice QR Code',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Add QR codes to invoices for quick payment reference',
    'description': """
Invoice QR Code Generator
=========================
This module adds QR codes to invoices containing:
- Invoice number
- Amount due
- Due date
- Payment reference

The QR code can be scanned by banking apps for quick payments.

Features:
- Automatic QR generation for posted invoices
- Configurable per invoice (show/hide)
- Support for multiple currencies
- Compatible with standard invoice reports
- Easy to customize QR data format

Technical:
- Uses qrcode library for generation
- Stores QR as computed binary field
- Extends standard account.move model
    """,
    'author': 'Dynamic Partners',
    'website': 'https://dynamicpartners.es',
    'license': 'LGPL-3',
    'depends': ['account'],
    'external_dependencies': {
        'python': ['qrcode'],
    },
    'data': [
        'views/account_move_views.xml',
        'views/report_invoice.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'dp_invoice_qr/static/src/css/qr_style.css',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 29.00,
    'currency': 'EUR',
}
