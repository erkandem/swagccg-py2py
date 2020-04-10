"""
auto-generated 2020-04-10 18:19:18
... using [swagccg-py2py](https://erkandem.github.io/swagccg-py2py)' version 0.3.3

your module level doc-string goes here
"""

# #######################################################################
# DO NOT MODIFY THIS FILE!
# Your changes will be lost if you rerun ``make_client.py``! 
# Edit the template!
# #######################################################################

from datetime import datetime as dt, timedelta
import json
import urllib
import urllib3
import certifi
import warnings


class MyClientClass(object):
    """your client class level doc-string goes here"""

    def __init__(self, deployment='remote'):
        if deployment == 'remote':
            self.API_PORT = '80'
            self.API_URL_BASE = 'petstore.swagger.io'
            self.API_PROTOCOL = 'https'
        elif deployment == 'local':
            self.API_PORT = '5000'
            self.API_URL_BASE = '127.0.0.1'
            self.API_PROTOCOL = 'http'

        self.BASE_PATH = '/api'
        self.LOGIN_TIMESTAMP = None
        self.API_TOKEN = None
        self.REFRESH_TIMESTAMP = None

        self.AUTH_HEADER_NAME = 'Authorization'
        self.AUTH_PREFIX = 'Bearer '  # mind the whitespace
        self.AUTH_TOKEN_KEY = 'access_token'
        self.AUTH_TOKEN_KEY_REFRESH = 'refreshed_token'
        self.REFRESH_KEY = 'token'

        if self.API_PORT == '80':
            self.API_URL = f'{self.API_PROTOCOL}://{self.API_URL_BASE}'
        else:
            self.API_URL = f'{self.API_PROTOCOL}://{self.API_URL_BASE}:{self.API_PORT}'

        if self.API_PROTOCOL == 'https':
            self.http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )
        else:
            self.http = urllib3.PoolManager()

        self.API_LOGIN_URL = f'{self.API_URL}{self.BASE_PATH}/login'
        self.API_REFRESH_URL = f'{self.API_URL}{self.BASE_PATH}/refresh'
        self.API_BASE_URL = f'{self.API_URL}{self.BASE_PATH}'

    def __dir__(self):
        method_names = [
            'get_find_pets_r',
            'post_add_pet_r',
            'get_find_pet_by_id_r',
            'delete_pet_r'
        ]
        return method_names
    
    def login_with_api(self, *, body, headers=None, **kwargs):
        """
        login with the target API and save the JWT token within the class
        
        Args:
            data: login data externally supplied
            body: data to be sent in body (typically credentials)
            headers: option to supply custom headers if needed
        """
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        else:
            if 'content-type' not in [h.lower() for h in headers]:
                headers['Content-Type'] = 'application/json'
        r = self._do_call(
                method='POST',
                url=self.API_LOGIN_URL,
                headers=headers,
                body=body,
                pass_through=True,
                **kwargs
        )
        if r.status == 200:
            res = json.loads(r.data.decode('utf-8'))
            self.API_TOKEN = res[self.AUTH_TOKEN_KEY]
            self.LOGIN_TIMESTAMP = dt.now()
            self.REFRESH_TIMESTAMP = None
        else:
            print(f'login failed \nstatus:{r.status} \n \nurl: {self.API_LOGIN_URL}'
                  '\nIs the username and password correct?')

    # -----------------------------------------------------------------------
    # ---------- Token Management
    # -----------------------------------------------------------------------

    def is_it_time_to_refresh_the_token(self):
        """
        Return True or False depending on the ``LOGIN_TIMESTAMP`` for the
        first refresh or the ``REFRESH_TIMESTAMP`` if the JWT was already
        refreshed once
        
        expiry is server specific
        """
        if self.REFRESH_TIMESTAMP is None:
            if (self.LOGIN_TIMESTAMP + timedelta(hours=10)) < dt.now():
                self.refresh_the_login()
                return True
            else:
                return False
        else:
            if (self.REFRESH_TIMESTAMP + timedelta(hours=10)) < dt.now():
                self.refresh_the_login()
                return True
            else:
                return False

    def refresh_the_login(self):
        """ server specific refresh routine"""
        encoded_data = json.dumps({'token': self.API_TOKEN}).encode('utf-8')
        r = self.http.request(
                'POST',
                self.API_REFRESH_URL,
                headers={'Content-Type': 'application/json'},
                body=encoded_data
        )
        res = json.loads(r.data.decode('utf-8'))
        self.API_TOKEN = res[self.AUTH_TOKEN_KEY_REFRESH]
        self.REFRESH_TIMESTAMP = dt.now()
    
    def _add_auth_header(self, headers=None):
        """ adds the preconfigured authorization header """
        if headers is None:
            headers = dict()
        headers[self.AUTH_HEADER_NAME] = f'{self.AUTH_PREFIX}{self.API_TOKEN}'
        return headers

    def _do_call(self, method=None, url=None, headers=None, fields=None, body=None, **kwargs):
        """
        A way to separate each resource from the actual request dispatching point
        Response is assumed to be json by default. any other mapping can be hooked here.

        Use ``pass_through = True`` to receive the untouched response object

        Args:
            method (str): HTTP-Method
            url (str): endpoint
            headers (dict): each key:value pair represents one header field:value. Don't nest!
            fields (dict):  each key:value pair will be urlencoded and passed as query string. Don't nest!
            body (dict): will be encoded to JSON and bytes afterwards
                         You can get a urlencoding by setting
                         'Content-Type': 'application/x-www-form-urlencoded'

        """

        headers = self._add_auth_header(headers)
        if body is not None and method in ['POST', 'PUT', 'PATCH']:
            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/json'
                r = self.http.request(
                        method=method,
                        url=url,
                        body=self._encode(body),
                        headers=headers
                    )
            else:
                if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                    r = self.http.urlopen(
                            method,
                            url,
                            body=self._encode(body, 'url'),
                            headers=headers
                    )
                elif headers['Content-Type'] == 'application/json':
                    r = self.http.request(
                            method=method,
                            url=url,
                            body=self._encode(body),
                            headers=headers
                    )
                else:
                    msg = f''' The Content-Type header was set to {headers['Content-Type']}\n
                    However, anything else than 'application/json' or 'application/x-www-form-urlencoded'\n
                    is not accounted for in the client.\n If you would like to add it look for:\n\n
                    client_point_of_execution_f to build the logic\n
                    client_encoding_decoding_point_f for handling encoding\n\n
                    -1 (negative one) was returned to avoid a RunTimeError'''
                    warnings.warn(msg)
                    return -1
        else:
            r = self.http.request_encode_url(
                    method=method,
                    url=url,
                    headers=headers,
                    fields=fields
            )
        if kwargs.get('pass_through'):
            return r

        if r.status == 200:
            if len(r.data) > 0:
                return self._decode(r.data)
            else:
                return r.status
        elif r.status == 401:
            self.refresh_the_login()
            return 401
        else:
            return -1
    
    def _encode(self, data, format=None):
        """
        Abstracted encoding point. Mount your custom function.
        Focus here is on built in JSON.

        Args:
            data(): python object
            format(str): json or url

        Returns:
            data_encoded: :func:`json.dumps` and encode from utf-8 to binary

        """
        if type(data) is bytes:
            return data
        if format == 'url':
            return (urllib.parse.urlencode(data)).encode('utf-8')
        if format is None:
            return (json.dumps(data)).encode('utf-8')
        elif format == 'json':
            return (json.dumps(data)).encode('utf-8')
        else:
            msg = f"received format = {format}.\nUse 'json' or 'url'.\n 'json' is default."
            raise NotImplementedError(msg)

    def _decode(self, data):
        """
        abstracted decoding point 
        Mount your custom function. Focus here is on JSON.

        Args:
            data: python object (dict, list, ...)

        Returns:
           data_decoded: first decode from binary to utf-8 and parse with 
                         built-in :func:`json.loads`
        """

        return json.loads(data.decode('utf-8')) 
    
    def get_find_pets_r(self, headers=None, body=None, fields_data=None, **kwargs):
        """   """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/pets',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_add_pet_r(self, headers=None, body=None, fields_data=None, **kwargs):
        """   """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/pets',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_find_pet_by_id_r(self, id, headers=None, body=None, fields_data=None, **kwargs):
        """   """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/pets/{id}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def delete_pet_r(self, id, headers=None, body=None, fields_data=None, **kwargs):
        """   """
        r = self._do_call(
                method='DELETE',
                url=f'{self.API_BASE_URL}/pets/{id}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
