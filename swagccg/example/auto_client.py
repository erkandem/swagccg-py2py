# Autogenerated 2019-02-15 22:16:39
# EDIT THE TEMPLATE INSTEAD OF THIS FILE
# IF YOU RERUN `make_client.py` YOUR CHANGES HERE WILL BE LOST
# LOOOOOOOOOOST!

try:
    import urllib3
except ImportError:
    raise ImportError(f'Make sure that there is no other file shadowing urllib3')
try:
    import certifi
except ImportError:
    raise ImportError(f'Make sure that there is no other file shadowing certifi')
try:
    import json
except ImportError:
    raise ImportError(f'Make sure that there is no other file shadowing json')
try:
    from datetime import datetime as dt, timedelta
except ImportError:
    raise ImportError(f'Make sure that there is no other file shadowing datetime, dt, or timedelta')


class MyClientClass(object):
    """ 
    Who needs SwaggerHub anyway ? 
    """
    # 'DELETE'? 
    methods_using_body = ['POST', 'PUT', 'PATCH']

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

        self.API_ENDPOINTS = []  # unused
        
        if self.API_PORT == '80':
            self.API_URL = f'{self.API_PROTOCOL}://{self.API_URL_BASE}'
        else:
            self.API_URL = f'{self.API_PROTOCOL}://{self.API_URL_BASE}:{self.API_PORT}'
        
        if self.API_PROTOCOL == 'https':
            self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                            ca_certs=certifi.where())
        else:
            self.http = urllib3.PoolManager()

        self.API_LOGIN_URL = f'{self.API_URL}/login'
        self.API_REFRESH_URL = f'{self.API_URL}/refresh'
        self.API_BASE_URL = f'{self.API_URL}{self.BASE_PATH}'
    
    def login_with_api(self, data):
        """ login with the target API and save the JWT token within the class
            .. param data:: login data externally supplied
        """
        encoded_data = json.dumps(data).encode('utf-8')
        r = self.http.request('POST',
                              self.API_LOGIN_URL,
                              headers={'Content-Type': 'application/json'},
                              body=encoded_data)
        if r.status == 200:
            res = json.loads(r.data.decode('utf-8'))
            self.API_TOKEN = res[self.AUTH_TOKEN_KEY]
            # print(self.API_TOKEN)
            self.LOGIN_TIMESTAMP = dt.now()
            self.REFRESH_TIMESTAMP = None
        else:
            print(f'login failed =/: \nstatus:{r.status} \nmessage: {r.msg} \nurl {r._request_url}')
    
    # -----------------------------------------------------------------------
    # ---------- Token Management
    # -----------------------------------------------------------------------
    
    def is_it_time_to_refresh_the_token(self):
        """ Return True or False depending on the ``LOGIN_TIMESTAMP`` for the
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
        r = self.http.request('POST',
                              self.API_REFRESH_URL,
                              headers={'Content-Type': 'application/json'},
                              body=encoded_data)
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
        """
        headers = self._add_auth_header(headers)
        if method in self.methods_using_body and body is not None:
            body = (json.dumps(body)).encode('utf-8')
            r = self.http.request(method=method,
                                  url=url,
                                  headers=headers,
                                  body=body)
        else:
            r = self.http.request_encode_url(method=method,
                                             url=url,
                                             headers=headers,
                                             fields=fields)
        # no processing whatsoever
        if 'pass_through' in kwargs:
            if kwargs['pass_through']:
                return r

        # very basic response code handling
        if r.status == 200:
            decoded = r.data.decode('utf-8')
            if len(decoded) > 0:
                return json.loads(decoded)
            else:
                return 200
        elif r.status == 401:
            self.refresh_the_login()
            return 0
        else:
            return 0
    
    def get_find_pets_r(self, headers=None, body=None, fields_data=None, **kwargs):
        """   """
        r = self._do_call(method='GET',
                          url=f'{self.API_BASE_URL}/pets',
                          headers=headers,
                          body=body,
                          fields=fields_data,
                          **kwargs)
        return r
    
    def post_add_pet_r(self, headers=None, body=None, fields_data=None, **kwargs):
        """   """
        r = self._do_call(method='POST',
                          url=f'{self.API_BASE_URL}/pets',
                          headers=headers,
                          body=body,
                          fields=fields_data,
                          **kwargs)
        return r
    
    def get_find_pet_by_id_r(self, id, headers=None, body=None, fields_data=None, **kwargs):
        """   """
        r = self._do_call(method='GET',
                          url=f'{self.API_BASE_URL}/pets/{id}',
                          headers=headers,
                          body=body,
                          fields=fields_data,
                          **kwargs)
        return r
    
    def delete_pet_r(self, id, headers=None, body=None, fields_data=None, **kwargs):
        """   """
        r = self._do_call(method='DELETE',
                          url=f'{self.API_BASE_URL}/pets/{id}',
                          headers=headers,
                          body=body,
                          fields=fields_data,
                          **kwargs)
        return r
     