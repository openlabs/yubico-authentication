# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
{
    'name': 'Yubico Authentication',
    'description': """
        Replaces standard authentication with Yubico OTPs
    """,
    'depends': ['res'],
    'xml': [
        'user.xml',
        'configuration.xml',
        ],
    'version': '1.8.2',
    'author': 'Openlabs Technologies & Consulting (P) LTD',
    'email': 'info@openlabs.co.in',
    'website': 'http://openlabs.co.in/',
}
