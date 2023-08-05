"""
Este modulo sirve para crear un plugin para bottle que active la autentificacion por jwt

modo de uso
>>> def validation(auth, auth_value):
...   return True
>>>
>>> pl = JwtPlugin(validation)
>>> token = pl.encode({'data': 'value'}, subject = 'tester')
>>> for key, value in ((key, value) for key, value in pl.decode(token).items() if key not in ('iat', 'exp', 'jti')):
...     print(key, value)
data value
iss bottle-jwt
aud ['bottle-jwt']
sub tester
"""

from bottle import request, redirect, abort, PluginError
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, encode as jwt_encode, decode as jwt_decode
import bottle_jwt_version

try:
    import secrets
    TOKEN_SAFE = secrets.token_urlsafe(64)
    TOKEN_ID = lambda: secrets.token_hex(16)
except ImportError: # Python 2.x suport
    import os
    import base64
    TOKEN_SAFE = base64.b64encode(os.urandom(64))
    TOKEN_ID = lambda: os.urandom(16).hex()

__project__ = "bottle-pyjwt"
__version__ = bottle_jwt_version.version
__author__ = "Lorenzo A. Garcia Calzadilla"
__author_email__ = "lorenzogarciacalzadilla@gmail.com"
__license__ = "MIT"
__description__ = "El plugin de bottle-pyjwt permite usar autentificacion mediante token usando el estandar java jwt"

class JwtPlugin(object):
    name = 'JwtPlugin'
    api = 2
    keyword = 'auth'

    def __init__(self, validation, key = TOKEN_SAFE, fail_redirect = '/login', ttl = 60*10, algorithm="HS512", headers=None, json_encoder=None, options = None, verify = True, audience = [], issuer = 'bottle-jwt'):
        self.validation = validation

        self.key = key
        self.algorithm = algorithm
        self.headers = headers
        self.json_encoder = json_encoder
        self.options = options
        self.verify = verify
        self.issuer = issuer
        self.audience = audience + [issuer]

        self.fail_redirect = fail_redirect
        self.ttl = ttl

    def encode(self, payload, subject = "", key = None, algorithm = None, headers = None, json_encoder = None, issuer = None, audience = [], jwt_id = None, ttl = None):
        """
        Funcion para crear un token
        """
        if not isinstance(payload, dict):
            raise TypeError('Expecting a mapping object, as JWT only supports '
                            'JSON objects as payloads.')

        payload['iat'] = payload.get('iat', datetime.utcnow()) # Marca temporal en que el JWT fue emitido
        payload['exp'] = payload.get('exp', payload['iat'] + timedelta(seconds = ttl or self.ttl)) # Marca temporal luego de la cual el JWT caduca
        payload['iss'] = payload.get('iss', issuer or self.issuer) # Proveedor de identidad que emitio el JWT
        payload['aud'] = payload.get('aud', audience or self.audience) # Audiencia o receptores para lo que el JWT fue emitido
        payload['sub'] = payload.get('sub', subject) # Objeto o usuario en nombre del cual fue emitido el JWT
        payload['jti'] = payload.get('jti', jwt_id or TOKEN_ID()) # Identificador unico del token


        key = key or self.key
        algorithm = algorithm or self.algorithm
        headers = headers or self.headers
        json_encoder = json_encoder or self.json_encoder

        return jwt_encode(payload, key, algorithm, headers, json_encoder)

    def decode(self, token, key = None, verify = None, algorithm = None, options = None, audience = [], issuer = None, leeway = 0, **kwargs):
        key = key or self.key
        algorithm = algorithm or self.algorithm
        options = options or self.options
        verify = verify or self.verify
        issuer = issuer or self.issuer
        audience = audience + [issuer]

        return jwt_decode(token, key, verify, algorithm, options, audience = audience, issuer = issuer, leeway = leeway, **kwargs)

    def get_token(self):
        '''
        Funcion que evalua si existe un token en el request
        '''
        # Se prueba con query, con form y con cookie
        token = request.params.get('access_token', request.get_cookie('access_token'))

        # Se prueba con el header
        auth = request.get_header('Authorization').split(" ", 1)
        if len(auth) == 2 and auth[0].lower() == "bearer":
            token = auth[1]

        return token

    def get_auth(self, fail_redirect = None):
        """
        Funcion que evalua la autorizacion del token
        """
        token = self.get_token()
        if not token:
            self.__get_error(fail_redirect, 403, "Forbidden")

        try:
            decoded = self.decode(token)
        except ExpiredSignatureError as e:
            self.__get_error(fail_redirect, 403, "Forbidden, expired token")
        else:
            self.__get_error(fail_redirect, 403, "Forbidden, bad token")

        decoded['token'] = token
        return decoded

    def __get_error(self, fail_redirect = None, code = 500, message = "Internal Server Error"):
        if isinstance(fail_redirect, str) and fail_redirect:
            redirect(fail_redirect)
        abort(code, message)

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, JwtPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another %s plugin with conflicting settings (non-unique keyword)." % self.name)
            elif other.name == self.name:
                self.name += '_%s' % self.keyword

        self.key = app.config.get('jwt.key', self.key)
        self.algorithm = app.config.get('jwt.algorithm', self.algorithm)
        self.headers = app.config.get('jwt.headers', self.headers)
        self.options = app.config.get('jwt.options', self.options)
        self.verify = app.config.get('jwt.verify', self.verify)
        self.issuer = app.config.get('jwt.issuer', self.issuer)
        self.audience = app.config.get('jwt.audience', self.audience)

        self.fail_redirect = app.config.get('jwt.redirect', self.fail_redirect)
        self.ttl = app.config.get('jwt.ttl', self.ttl)

    def apply(self, callback, route):
        auth_value = route.config.get(self.keyword, None)
        if not auth_value:
            return callback

        fail_redirect = route.config.get('fail_redirect', self.fail_redirect)

        auth = self.get_auth(fail_redirect)
        if self.validation(auth, auth_value):
            request.auth = auth
            request.jwt = self

            return callback
        else:
            self.__get_error(fail_redirect, 403, "Forbidden")

Plugin = JwtPlugin

if __name__ == "__main__":
    import doctest
    if not doctest.testmod().failed:
        print('All test OK')
