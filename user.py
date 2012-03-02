# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
'''
Yubico Yubikey based authentication

The yubikey authentication is performed only if the user has atleast one 
yubikey OTP registered against him. If there are none the authentication
falls back into password based authentication. The absense of the configuration
(client ID and Key) also results in the same behaviour (falling back to 
password based authentication). 

Getting the OTP as a separate argument from client to the get_login method 
would require several hacks including trytond/security and trytond/server. 
This could later be improved if the system wants to provide two/multi factor 
authentication by default. For now the design accepts a password which consists 
of the password concatenated with the OTP and separated by the pipe character 
(|).

:copyright: (c) 2010-2011 by Sharoon Thomas.
:copyright: (c) 2010-2011 by Openlabs Technologies & Consulting (P) LTD
:license: GPLv3, see LICENSE for more details
'''

from yubicoclient import YubicoClient
from trytond.model import ModelView, ModelSQL, fields


class User(ModelSQL, ModelView):
    """Alter login schema to use yubikey.

    If there are no regsitered keys against the user, then the login fallsback
    to traditional password based authentication.
    """
    _name = 'res.user'

    yubikeys = fields.One2Many('res.user.yubikey', 'user', 'Yubikeys')

    def get_login(self, login, password):
        '''
        :param login: the login name
        :param password: the password
        :return: integer
        '''
        config_obj = self.pool.get('yubico.configuration')

        config = config_obj.browse(1)

        # Identify the User from the login provided alone. Required to check
        # the type of authentication the user has to satisfy.
        user_id, _, _ = self._get_login(login)
        if not user_id:
            return 0

        user = self.browse(user_id)
        if not user.yubikeys or not config.client_id:
            # If there are no yubikeys registered against the user (which is 
            # required to identify the owner of the key) |OR|
            # If there is no configuration settings then fallback to password
            # based authentication
            return super(User, self).get_login(login, password)

        if not config.single_factor and '|' not in password:
            # If pipe is not there then it's not valid anyway
            return 0

        if not config.single_factor:
            password, otp = password.rsplit('|', 1)

            # First of two factor authentication is password itself
            user_id = super(User, self).get_login(login, password)
            if user_id == 0:
                return 0
        else:
            # In single factor the password is otp alone
            otp = password

        # Second of two factor authentication using yubikey
        for key in user.yubikeys:
            # Check if given OTP matches any of the keys registered against the
            # user and chose that key to validate.
            if key.otp[:-32] == otp[:-32]:
                break
        else:
            return 0

        # Check if OTP is verified
        yubico_client = YubicoClient(config.client_id, config.signature)
        return user_id if yubico_client.verify(otp) else 0

User()


class UserYubikey(ModelSQL, ModelView):
    """A list of the Yubikeys of the user is stored to ensure a match of the 
    key being used to the user.
    YubiKey OTP contains as the initial part, an identity of the YubiKey, 
    and it can be used to identify the user. The identity part is the same 
    for every OTP, and it is the initial 2-16 modhex characters of the OTP. 
    """
    _name = 'res.user.yubikey'
    _description = "Yubikeys of users"

    user = fields.Many2One('res.user', 'User', required=True)
    otp = fields.Char('OTP', required=True)

    # TODO: A constraint which verifies that a certain key is not entered
    # twice as its not optimal (though it works).This can be done by testing 
    # for identity from given OTP.

UserYubikey()
