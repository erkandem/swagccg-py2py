"""
auto-generated 2020-12-27 17:27:13
... using [swagccg-py2py](https://erkandem.github.io/swagccg-py2py)' version 0.4.0

your module level doc-string goes here
"""

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


class MyClientClass(object):
    """your client class level doc-string goes here"""

    def __init__(self, deployment: str = 'remote', base_path: str = None):
        if deployment == 'remote':
            self.API_PORT = '80'
            self.API_URL_BASE = 'petstore.swagger.io'
            self.API_PROTOCOL = 'https'
        elif deployment == 'local':
            self.API_PORT = '5000'
            self.API_URL_BASE = '127.0.0.1'
            self.API_PROTOCOL = 'http'

        self.BASE_PATH = '/v2'
        if base_path:
            self.BASE_PATH = base_path

        self.LOGIN_TIMESTAMP = None
        self.API_TOKEN = None

        self.AUTH_HEADER_NAME = 'Authorization'
        self.AUTH_PREFIX = 'Bearer '  # mind the whitespace
        self.AUTH_TOKEN_KEY = 'access_token'

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
        self.API_BASE_URL = f'{self.API_URL}{self.BASE_PATH}'

    def __dir__(self) -> t.List[str]:
        method_names = [
            'post_upload_file_r',
            'post_add_pet_r',
            'put_update_pet_r',
            'get_find_pets_by_status_r',
            'get_find_pets_by_tags_r',
            'get_pet_by_id_r',
            'post_update_pet_with_form_r',
            'delete_pet_r',
            'post_place_order_r',
            'get_order_by_id_r',
            'delete_order_r',
            'get_inventory_r',
            'post_create_users_with_array_input_r',
            'post_create_users_with_list_input_r',
            'get_user_by_name_r',
            'put_update_user_r',
            'delete_user_r',
            'get_login_user_r',
            'get_logout_user_r',
            'post_create_user_r'
        ]
        return method_names
    
    def login_with_api(
        self, 
        *,
        body, 
        headers: t.Dict[str, t.Any] = None,
        **kwargs: t.Dict[str, t.Any],
    ):
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
                **kwargs
        )
        if r.status == 200:
            res = json.loads(r.data.decode('utf-8'))
            self.API_TOKEN = res[self.AUTH_TOKEN_KEY]
            self.LOGIN_TIMESTAMP = dt.now()
        else:
            print(f'login failed \nstatus:{r.status} \n \nurl: {self.API_LOGIN_URL}'
                  '\nIs the username and password correct?')
    
    def _add_auth_header(
        self, 
        headers: t.Union[None, t.Dict[str, t.Any]] = None,
    ) -> t.Dict[str, t.Any]:
        """ adds the preconfigured authorization header """
        if headers is None:
            headers = {}
        headers[self.AUTH_HEADER_NAME] = f'{self.AUTH_PREFIX}{self.API_TOKEN}'
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
        """
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

        """
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
                    msg = f''' The Content-Type header was set to {headers['Content-Type']}\n
                    However, anything else than 'application/json' or 'application/x-www-form-urlencoded'\n
                    is not accounted for in the client.\n If you would like to add it, look for:\n\n
                    "_do_call" to hook the logic\n
                    client_encoding_decoding_point_f for handling encoding\n\n
                    '''
                    raise NotImplementedError(msg)
        else:
            r = self.http.request_encode_url(
                    method=method,
                    url=url,
                    headers=headers,
                    fields=fields
            )
        return r
    
    def _encode(self, data, format: str = None) -> bytes:
        """
        Abstracted encoding point. Mount your custom function.
        Main focus here is on building a JSON or URL/"percent" encoded bytes.

        Args:
            data(): python object
            format(str): `json` or `url` 

        Returns:
            data_encoded: :func:`json.dumps` and encode from utf-8 to binary

        """
        if isinstance(data, bytes):
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

    def _decode(self, data: bytes):
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
    
    def post_upload_file_r(
       self,
       petId,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ uploads an image """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/pet/{petId}/uploadImage',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_add_pet_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Add a new pet to the store """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/pet',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def put_update_pet_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Update an existing pet """
        r = self._do_call(
                method='PUT',
                url=f'{self.API_BASE_URL}/pet',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_find_pets_by_status_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Finds Pets by status """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/pet/findByStatus',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_find_pets_by_tags_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Finds Pets by tags """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/pet/findByTags',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_pet_by_id_r(
       self,
       petId,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Find pet by ID """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/pet/{petId}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_update_pet_with_form_r(
       self,
       petId,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Updates a pet in the store with form data """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/pet/{petId}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def delete_pet_r(
       self,
       petId,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Deletes a pet """
        r = self._do_call(
                method='DELETE',
                url=f'{self.API_BASE_URL}/pet/{petId}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_place_order_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Place an order for a pet """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/store/order',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_order_by_id_r(
       self,
       orderId,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Find purchase order by ID """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/store/order/{orderId}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def delete_order_r(
       self,
       orderId,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Delete purchase order by ID """
        r = self._do_call(
                method='DELETE',
                url=f'{self.API_BASE_URL}/store/order/{orderId}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_inventory_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Returns pet inventories by status """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/store/inventory',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_create_users_with_array_input_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Creates list of users with given input array """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/user/createWithArray',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_create_users_with_list_input_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Creates list of users with given input array """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/user/createWithList',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_user_by_name_r(
       self,
       username,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Get user by user name """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/user/{username}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def put_update_user_r(
       self,
       username,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Updated user """
        r = self._do_call(
                method='PUT',
                url=f'{self.API_BASE_URL}/user/{username}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def delete_user_r(
       self,
       username,
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Delete user """
        r = self._do_call(
                method='DELETE',
                url=f'{self.API_BASE_URL}/user/{username}',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_login_user_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Logs user into the system """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/user/login',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def get_logout_user_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Logs out current logged in user session """
        r = self._do_call(
                method='GET',
                url=f'{self.API_BASE_URL}/user/logout',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
    
    def post_create_user_r(
       self,
       
       headers: t.Dict[str, str] = None,
       body: JSONEncodable = None,
       fields_data: t.Dict[str, str] = None,
       **kwargs
    ):
        """ Create user """
        r = self._do_call(
                method='POST',
                url=f'{self.API_BASE_URL}/user',
                headers=headers,
                body=body,
                fields=fields_data,
                **kwargs
        )
        return r
