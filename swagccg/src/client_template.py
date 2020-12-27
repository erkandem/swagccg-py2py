from datetime import datetime as dt
from . import __version__
import typing as t


def client_imports_f() -> str:
    """
    Creates the string to import the client dependencies and
    a default module doc string. Usually the first part
    of the client module.

    Returns:
        str: import statements string ready to be appended to client module
    """
    time_stamp = dt.now().strftime('%Y-%m-%d %H:%M:%S')

    py_code = f'''\"\"\"
auto-generated {time_stamp}
... using [swagccg-py2py](https://erkandem.github.io/swagccg-py2py)' version {__version__}

your module level doc-string goes here
\"\"\"

# #######################################################################
# DO NOT MODIFY THIS FILE!
# Your changes will be lost if you rerun ``make_client.py``! 
# Edit the template!
# #######################################################################

from datetime import datetime as dt
import json
import typing as t
import urllib
import urllib3
from urllib3.response import HTTPResponse
import certifi


JSONEncodable = t.Union[t.List[t.Any], t.Dict[str, t.Any]]
'''
    return py_code


def client_class_def_template_f(args: t.Dict[str, t.Any]) -> str:
    """
    Args:
        args (dict): desired name of client class name default:MyApiClient

    Returns:
        str: class definition string ready to be appended to client-module
    """
    py_code = f'''

class {args['class_name']}(object):
    \"\"\"your client class level doc-string goes here\"\"\"

    def __init__(self, deployment: str = 'remote', base_path: str = None):
        if deployment == 'remote':
            self.API_PORT = '{args["api_port_remote"]}'
            self.API_URL_BASE = '{args["api_url_base_remote"]}'
            self.API_PROTOCOL = '{args["api_protocol_remote"]}'
        elif deployment == 'local':
            self.API_PORT = '{args["api_port_local"]}'
            self.API_URL_BASE = '{args["api_url_base_local"]}'
            self.API_PROTOCOL = '{args["api_protocol_local"]}'

        self.BASE_PATH = '{args["basePath"]}'
        if base_path:
            self.BASE_PATH = base_path

        self.LOGIN_TIMESTAMP = None
        self.API_TOKEN = None

        self.AUTH_HEADER_NAME = 'Authorization'
        self.AUTH_PREFIX = 'Bearer '  # mind the whitespace
        self.AUTH_TOKEN_KEY = 'access_token'

        if self.API_PORT == '80':
            self.API_URL = f'{{self.API_PROTOCOL}}://{{self.API_URL_BASE}}'
        else:
            self.API_URL = f'{{self.API_PROTOCOL}}://{{self.API_URL_BASE}}:{{self.API_PORT}}'

        if self.API_PROTOCOL == 'https':
            self.http = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where()
            )
        else:
            self.http = urllib3.PoolManager()

        self.API_LOGIN_URL = f'{{self.API_URL}}{{self.BASE_PATH}}/login'
        self.API_BASE_URL = f'{{self.API_URL}}{{self.BASE_PATH}}'

    # def __dir__(self):

    def login_with_api(
        self, 
        *,
        body, 
        headers: t.Dict[str, t.Any] = None,
        **kwargs: t.Dict[str, t.Any],
    ):
        \"\"\"
        login with the target API and save the JWT token within the class
        
        Args:
            data: login data externally supplied
            body: data to be sent in body (typically credentials)
            headers: option to supply custom headers if needed
        \"\"\"
        if headers is None:
            headers = {{'Content-Type': 'application/json'}}
        else:
            if 'content-type' not in [h.lower() for h in headers]:
                headers['Content-Type'] = 'application/json'
        r = self._do_call(
                method='POST',
                url=self.API_LOGIN_URL,
                headers=headers,
                body=body,
                **kwargs
        )
        if r.status == 200:
            res = json.loads(r.data.decode('utf-8'))
            self.API_TOKEN = res[self.AUTH_TOKEN_KEY]
            self.LOGIN_TIMESTAMP = dt.now()
        else:
            print(f'login failed \\nstatus:{{r.status}} \\n \\nurl: {{self.API_LOGIN_URL}}'
                  '\\nIs the username and password correct?')
    '''
    return py_code


def dir_template_f(method_names: []) -> str:
    """
    generate `__dir__` method code to deliver
    a list of all methods which are mapped
    to an  API routes
    """
    method_names_ = "'" + "',\n            '".join(method_names) + "'"
    return f'''
    def __dir__(self) -> t.List[str]:
        method_names = [
            {method_names_}
        ]
        return method_names
    '''


def client_encoding_decoding_point_f() -> str:
    """
    provides method code to encode and decode response data
    """
    py_code = '''
    def _encode(self, data, format: str = None) -> bytes:
        \"\"\"
        Abstracted encoding point. Mount your custom function.
        Main focus here is on building a JSON or URL/"percent" encoded bytes.

        Args:
            data(): python object
            format(str): `json` or `url` 

        Returns:
            data_encoded: :func:`json.dumps` and encode from utf-8 to binary

        \"\"\"
        if isinstance(data, bytes):
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

    def _decode(self, data: bytes):
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


def client_point_of_execution_f() -> str:
    """
    The idea is to separate details of the endpoint and transmitting the request.
    ``status_code`` handling could be placed or called here
    """
    py_code = f'''
    def _add_auth_header(
        self, 
        headers: t.Union[None, t.Dict[str, t.Any]] = None,
    ) -> t.Dict[str, t.Any]:
        \"\"\" adds the preconfigured authorization header \"\"\"
        if headers is None:
            headers = {{}}
        headers[self.AUTH_HEADER_NAME] = f'{{self.AUTH_PREFIX}}{{self.API_TOKEN}}'
        return headers

    def _do_call(
        self, 
        method: str = None, 
        url: str = None, 
        headers: t.Dict[str, str] = None,
        fields: t.Dict[str, t.Any] = None, 
        body: JSONEncodable = None,
        **kwargs: t.Dict[str, t.Any],
    ) -> HTTPResponse:
        \"\"\"
        A way to separate each resource from the actual request dispatching point
        Response is assumed to be json by default. 
        Good point to add hooks.

        Args:
            method (str): HTTP-Method
            url (str): endpoint
            headers (dict): each key:value pair represents one header field:value. Don't nest!
            fields (dict):  each key:value pair will be urlencoded and passed as query string. Don't nest!
            body (dict): will be encoded to JSON and bytes afterwards
                         You can get a urlencoding by setting
                         'Content-Type': 'application/x-www-form-urlencoded'

        \"\"\"
        r = HTTPResponse()
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
                    msg = f\'\'\' The Content-Type header was set to {{headers['Content-Type']}}\\n
                    However, anything else than 'application/json' or 'application/x-www-form-urlencoded'\\n
                    is not accounted for in the client.\\n If you would like to add it, look for:\\n\\n
                    "_do_call" to hook the logic\\n
                    client_encoding_decoding_point_f for handling encoding\\n\\n
                    \'\'\'
                    raise NotImplementedError(msg)
        else:
            r = self.http.request_encode_url(
                    method=method,
                    url=url,
                    headers=headers,
                    fields=fields
            )
        return r
    '''
    return py_code


def client_method_template_f(
        method_name: str = '',
        http_verb: str = '',
        api_path: str = '',
        doc_string: str = '',
        path_params_list: t.List[str] = None,
) -> str:
    """
     one size fits *most* method template

    Args:
        http_verb (str): `GET`, `POST`, `PUT`, `DELETE` and `PATCH`
        method_name (str): a valid python function name as a string
        api_path (str): a valid URL part which is joined with the `BASE_PATH`.
                  Can contain path parameters. Will be evaluated to a string.
        doc_string (str): some description of the method and or endpoint
        path_params_list (str): e.g. pagination is frequently used in the path

    Returns:
        str: a method code string ready to be appended to python-client-module
    """
    if path_params_list is not None and len(path_params_list) > 0:
        path_params = '\n       '.join(f'{p},' for p in path_params_list)
    else:
        path_params = ''
    py_code = f'''
    def {method_name}(
       self,
       {path_params}
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        \"\"\" {doc_string} \"\"\"
        r = self._do_call(
                method='{http_verb.upper()}',
                url=f'{{self.API_BASE_URL}}{api_path}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    '''
    return py_code
