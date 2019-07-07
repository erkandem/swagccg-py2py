from datetime import datetime as dt


def client_imports_f():
    """
    creates the string to import the dependecies
    Usually the first part of the client module
    :return: string, ready to append to python-module
    """
    time_stamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')

    py_code = f'''\"\"\"
auto-generated {time_stamp}
... using [swagccg-py2py](https://erkandem.github.io/swagccg-py2py)'

your module level doc-string goes here
\"\"\"

# #######################################################################
# DO NOT MODIFY THIS FILE!
# Your changes will be lost if you rerun ``make_client.py``! 
# Edit the template!
# #######################################################################

try:
    import urllib3
except ImportError:
    raise ImportError(f'Make sure that there is no other file shadowing urllib3')
try:
    import urllib
except ImportError:
    raise ImportError(f'Make sure that there is no other file shadowing urllib')
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
try:
    import warnings
except ImportError:
    raise ImportError(f'Make sure that there is no other file shadowing warnings')
'''
    return py_code


def client_class_def_template_f(args):
    """

    :param args: desired name of client class name default:MyApiClient
    :return: string, ready to append to python-module
    """
    py_code = f'''

class {args['class_name']}(object):
    \"\"\"your client class level doc-string goes here\"\"\"

    def __init__(self, deployment='remote'):
        if deployment == 'remote':
            self.API_PORT = '{args["api_port_remote"]}'
            self.API_URL_BASE = '{args["api_url_base_remote"]}'
            self.API_PROTOCOL = '{args["api_protocol_remote"]}'
        elif deployment == 'local':
            self.API_PORT = '{args["api_port_local"]}'
            self.API_URL_BASE = '{args["api_url_base_local"]}'
            self.API_PROTOCOL = '{args["api_protocol_local"]}'
        
        self.BASE_PATH = '{args["basePath"]}'
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
            self.API_URL = f'{{self.API_PROTOCOL}}://{{self.API_URL_BASE}}'
        else:
            self.API_URL = f'{{self.API_PROTOCOL}}://{{self.API_URL_BASE}}:{{self.API_PORT}}'
        
        if self.API_PROTOCOL == 'https':
            self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                            ca_certs=certifi.where())
        else:
            self.http = urllib3.PoolManager()

        self.API_LOGIN_URL = f'{{self.API_URL}}{{self.BASE_PATH}}/auth/login'
        self.API_REFRESH_URL = f'{{self.API_URL}}{{self.BASE_PATH}}/auth/refresh'
        self.API_BASE_URL = f'{{self.API_URL}}{{self.BASE_PATH}}'
    
    def login_with_api(self, data):
        \"\"\" login with the target API and save the JWT token within the class
            .. param data:: login data externally supplied
        \"\"\"
        encoded_data = json.dumps(data).encode('utf-8')
        r = self.http.request('POST',
                              self.API_LOGIN_URL,
                              headers={{'Content-Type': 'application/json'}},
                              body=encoded_data)
        if r.status == 200:
            res = json.loads(r.data.decode('utf-8'))
            self.API_TOKEN = res[self.AUTH_TOKEN_KEY]
            # print(self.API_TOKEN)
            self.LOGIN_TIMESTAMP = dt.now()
            self.REFRESH_TIMESTAMP = None
        else:
            print(f'login failed =/: \\nstatus:{{r.status}} \\nmessage: {{r.msg}} \\nurl {{r._request_url}}')
    
    # -----------------------------------------------------------------------
    # ---------- Token Management
    # -----------------------------------------------------------------------
    
    def is_it_time_to_refresh_the_token(self):
        \"\"\" Return True or False depending on the ``LOGIN_TIMESTAMP`` for the
        first refresh or the ``REFRESH_TIMESTAMP`` if the JWT was already
        refreshed once
        
        expiry is server specific
         \"\"\"
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
        \"\"\" server specific refresh routine\"\"\"
        encoded_data = json.dumps({{'token': self.API_TOKEN}}).encode('utf-8')
        r = self.http.request('POST',
                              self.API_REFRESH_URL,
                              headers={{'Content-Type': 'application/json'}},
                              body=encoded_data)
        res = json.loads(r.data.decode('utf-8'))
        self.API_TOKEN = res[self.AUTH_TOKEN_KEY_REFRESH]
        self.REFRESH_TIMESTAMP = dt.now()
    '''
    return py_code


def client_encoding_decoding_point_f():
    """move every call for parsing response data to a single method"""

    py_code = '''
    def _encode(self, data, format=None):
        \"\"\"
        Abstracted encoding point. Mount your custom function.
        Focus here is on built in JSON.
        
        Args:
            data(): python object
            format(str): json or url
        
        Returns:
            data_encoded: :func:`json.dumps` and encode from utf-8 to binary
            
        \"\"\"
        if type(data) is bytes:
            return data
        if format == 'url':
            return (urllib.parse.urlencode(data)).encode('utf-8')
        if format is None:
            return (json.dumps(data)).encode('utf-8')
        elif format == 'json':
            return (json.dumps(data)).encode('utf-8')
        else:
            msg = f"received format = {format}.\\nUse 'json' or 'url'.\\n 'json' is default."
            raise NotImplementedError(msg)

    def _decode(self, data):
        \"\"\"
        abstracted decoding point 
        Mount your custom function. Focus here is on JSON.
        
        Args:
            data: python object (dict, list, ...)
        
        Returns:
           data_decoded: first decode from binary to utf-8 and parse with 
                         built-in :func:`json.loads`
        \"\"\"
        
        return json.loads(data.decode('utf-8')) 
    '''

    return py_code


def client_point_of_execution_f():
    """
    The idea is to separate details of the endpoint and transmitting the request.
    ``status_code`` handling could be placed or called here
    """
    py_code = f'''
    def _add_auth_header(self, headers=None):
        \"\"\" adds the preconfigured authorization header \"\"\"
        if headers is None:
            headers = dict()
        headers[self.AUTH_HEADER_NAME] = f'{{self.AUTH_PREFIX}}{{self.API_TOKEN}}'
        return headers

    def _do_call(self, method=None, url=None, headers=None, fields=None, body=None, **kwargs):
        \"\"\"
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

        \"\"\"
        
        headers = self._add_auth_header(headers)
        if body is not None and method in ['POST', 'PUT', 'PATCH']:
            if 'Content-Type' not in list(headers):
                headers['Content-Type'] = 'application/json'
                r = self.http.request(method=method,
                                      url=url,
                                      body=self._encode(body),
                                      headers=headers)
            else:
                if headers['Content-Type'] == 'application/x-www-form-urlencoded':
                    r = self.http.urlopen(method,
                                          url,
                                          body=self._encode(body, 'url'),
                                          headers=headers)
                elif headers['Content-Type'] == 'application/json':
                    r = self.http.request(method=method,
                                          url=url,
                                          body=self._encode(body),
                                          headers=headers)
                else:
                    msg = f\'\'\' The Content-Type header was set to {{headers['Content-Type']}}\\n
                    However, anything else than 'application/json' or 'application/x-www-form-urlencoded'\\n
                    is not accounted for in the client.\\n If you would like to add it look for:\\n\\n
                    client_point_of_execution_f to build the logic\\n
                    client_encoding_decoding_point_f for handling encoding\\n\\n
                    0 (zero) was returned to avoid a RunTimeError\'\'\'
                    warnings.warn(msg)
                    return 0
        else:
            r = self.http.request_encode_url(method=method,
                                             url=url,
                                             headers=headers,
                                             fields=fields)
        if 'pass_through' in kwargs:
            if kwargs['pass_through']:
                return r

        if r.status == 200:
            if len(r.data) > 0:
                return self._decode(r.data)
            else:
                return r.status
        elif r.status == 401:
            self.refresh_the_login()
            return 0
        else:
            return 0
    '''
    return py_code


def client_method_template_f(method_name='', http_verb='', api_path='', doc_string='', path_params=''):
    """
     one size fits *most* method template

    :param http_verb: GET, POST, PUT, DELETE and PATCH
    :param method_name: a valid python function name as a string
    :param api_path: a valid URL part which is joined with the BASE_PATH, can
                      contain parameters. Wil be evaluated to a string.
    :param doc_string: some description of the function and or endpoint
    :param path_params: e.g. pagination is frequently used in the path
    :return: string, ready to be appended to python-client-module
    """
    py_code = f'''
    def {method_name}(self{path_params}, headers=None, body=None, fields_data=None, **kwargs):
        \"\"\" {doc_string} \"\"\"
        r = self._do_call(method='{http_verb.upper()}',
                          url=f'{{self.API_BASE_URL}}{api_path}',
                          headers=headers,
                          body=body,
                          fields=fields_data,
                          **kwargs)
        return r
    '''
    return py_code

