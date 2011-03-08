# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
'''
    trytond_yubico_auth

Yubico Yubikey based authentication

:copyright: (c) 2010-2011 by Sharoon Thomas.
:copyright: (c) 2010-2011 by Openlabs Technologies & Consulting (P) LTD
:license: GPLv3, see LICENSE for more details
'''

from otcltools.yubikey import Yubikey
from trytond.model import ModelView, ModelSQL, fields


class User(ModelSQL, ModelView):
    """
    User
    ~~~~

    The login name of the user should be the email ID on Google
    Authentication services.

    The check is done against google docs, which is a quite common
    service used
    """
    _name = 'res.user'

    yubikeys = fields.One2Many('res.user.yubikey', 'user', 'Yubikeys')

    def get_login(self, login, password):
        '''
        Use yubikey authentication if it exists, else fall back to
        password based authentication

        :param login: the login name
        :param password: the password
        :return: integer
        '''
        config_obj = self.pool.get('yubico.configuration')

        config = config_obj.browse(1)
        user_id, user_password, salt = self._get_login(login)
        if not user_id:
            return 0
        user = self.browse(user_id)
        if not user.yubikeys or not config.client_id:
            return super(User, self).get_login(login, password)

        # Check if identity matches
        for key in user.yubikeys:
            if key.otp[:-32] == password[:-32]:
                break
        else:
            return 0

        # Check if OTP is verified
        yubikey_client = Yubikey(config.client_id, config.signature)
        return user_id if yubikey_client.verify(password) else 0

User()


class UserYubikey(ModelSQL, ModelView):
    "Yubikeys of users"
    _name = 'res.user.yubikey'
    _description = __doc__

    user = fields.Many2One('res.user', 'User', required=True)
    otp = fields.Char('OTP', required=True)

    # TODO: A constraint which verifies that a certain key is not entered
    # twice as its not optimal though works. This can be done by testing for
    # identity from given OTP

UserYubikey()
