# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
{
    'name': 'Yubico Authentication',
    'description': """
    Extends support for Two factor authentication in addition to the standard 
    password based authentication provided by Tryton
    """,
    'depends': [
        'res',
        ],
    'xml': [
        'user.xml',
        'configuration.xml',
        ],
    'version': '2.0.0.2',
    'author': 'Openlabs Technologies & Consulting (P) LTD',
    'email': 'info@openlabs.co.in',
    'website': 'http://openlabs.co.in/',
}
