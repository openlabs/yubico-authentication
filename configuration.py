# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
'''
    trytond_yubico_auth

Yubico Yubikey based authentication

:copyright: (c) 2010-2011 by Sharoon Thomas.
:copyright: (c) 2010-2011 by Openlabs Technologies & Consulting (P) LTD
:license: GPLv3, see LICENSE for more details
'''
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields


class Configuration(ModelSingleton, ModelSQL, ModelView):
    'Yubico Configuration'
    _name = 'yubico.configuration'
    _description = __doc__

    client_id = fields.Char('Client ID', required=True)
    signature = fields.Char('Signature')

Configuration()
