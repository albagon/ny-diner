import json
import os
from os import environ as env
from flask import request, _request_ctx_stack, abort, redirect
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# Configuration variables for Auth0
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv("AUTH0_AUDIENCE")

## AuthError Exception
'''
AuthError Exception
    A standardized way to communicate auth failure modes.
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header
'''
get_token_auth_header() method
    It should attempt to get the header from the request.
    It should raise an AuthError if no header is present.
    It should attempt to split bearer and the token.
    It should raise an AuthError if the header is malformed.
    Return the token part of the header.
'''
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        print('No Authorization header')
        abort(401)

    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        print('No 2 parts in header')
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        print('No bearer in header')
        abort(401)
    return header_parts[1]

'''
check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:restaurants')
        payload: decoded jwt payload

    It should raise an AuthError if permissions are not included in the payload.
    !!NOTE check your RBAC settings in Auth0.
    It should raise an AuthError if the requested permission string is not in
    the payload permissions array.
    Return true otherwise.
'''
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    if permission not in payload['permissions']:
        abort(401)
    return True

'''
verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    It should be an Auth0 token with key id (kid).
    It should verify the token using Auth0 /.well-known/jwks.json
    It should decode the payload from the token.
    It should validate the claims.
    Return the decoded payload.

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    print('unverified header', unverified_header)

    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
@requires_auth_p(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'get:restaurants')

    It should use the get_token_auth_header method to get the token.
    It should use the verify_decode_jwt method to decode the jwt.
    It should use the check_permissions method validate claims and check the
    requested permission.
    Return the decorator which passes the decoded payload to the decorated
    method.
'''
def requires_auth_p(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            print('jwt ', jwt)
            try:
                payload = verify_decode_jwt(jwt)
            except Exception:
                print('Payload unverified')
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
