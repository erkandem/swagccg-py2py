import os
# import dotenv
from datetime import datetime as dt
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# dotenv.load_dotenv(dotenv_path)

# python -m swagccg swagccg/examples/confi.json

# add a pet
from random import random
PET_ID = int(random()*(10**10))
print(f'petId: {PET_ID}')

BODY = {
    "id": PET_ID,
    "category": {"id": PET_ID, "name": "koalabaerchen"},
    "name": "koalabaerchen",
    "photoUrls": ["https://abcdefghijklmn.de"],
    "tags": [{"id": PET_ID,
              "name": "koalabaerchen"}],
    "status": "available"
}

HEADERS = {
    'Content-Type': 'application/json',
    'api-key': 'special-key'
}

COMMAND = 'python -m swagccg  --c swagccg/tests/test_confi.json'
STATUS = os.system(COMMAND)
if STATUS == 0:
    from swagccg.tests.auto_client import MyClientClass
else:
    raise OSError('Could not create the client')

# petstore specific settings
CLIENT = MyClientClass(deployment='remote')
CLIENT.API_TOKEN = 'special-key'
CLIENT.AUTH_HEADER_NAME = 'api-key'
CLIENT.AUTH_PREFIX = ''
CLIENT.AUTH_TOKEN_KEY = ''
CLIENT.AUTH_TOKEN_KEY_REFRESH = ''
CLIENT.REFRESH_KEY = ''


def test_client_creation():
    """
    items tested:
        - passing the commandline argument
        - reading the configuration file
        - reading the swagger file
        - writing the output
    """
    # response = subprocess.run(cmd, capture_output=True)
    # if response.returncode:
    #    print(response.stderr.decode('utf-8'))
    # assert response.returncode == 0
    assert STATUS == 0


def test_client_importing():
    """
    import the ClientClass from the client module.
    Thereafter, adjust the instance attributes to
    the requirements of the testAPI API and instantiate to ``CLIENT``.
    :return:
    """
    assert isinstance(CLIENT, MyClientClass)


class TestClientFunctionality(object):

    def test_post_with_json_body(self):
        r1 = CLIENT.post_add_pet_r(body=BODY, headers=HEADERS)
        assert r1 == BODY

    def get_path_parameter(self):
        """assure that the pet was created, auth required"""
        r2 = CLIENT.get_pet_by_id_r(petId=PET_ID)
        assert r2 == BODY

    def test_put_with_json_body(self):
        """ """
        BODY["photoUrls"] = ["https://updatedurl.de"]
        r3 = CLIENT.put_update_pet_r(body=BODY, headers=HEADERS)
        assert r3["photoUrls"] == ["https://updatedurl.de"]

    def test_post_with_query_string_1(self):
        """ """
        update = {
            'status': 'pending'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r4 = CLIENT.post_update_pet_with_form_r(petId=PET_ID, body=update, headers=headers)
        assert r4 == 200

    def test_get_path_param_1(self):
        """ """
        r5 = CLIENT.get_find_pets_by_status_r(fields_data={"status": "pending"})
        pet_ids = [item["id"] for item in r5]
        assert PET_ID in pet_ids

    def test_post_with_query_string_2(self):
        """ """
        update = {
            'status': 'sold'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r6 = CLIENT.post_update_pet_with_form_r(petId=PET_ID, body=update, headers=headers)
        assert r6 == 200

    def test_get_path_param_2(self):
        """ """
        r7 = CLIENT.get_find_pets_by_status_r(fields_data={"status": "sold"})
        pet_ids = [item["id"] for item in r7]
        assert PET_ID in pet_ids

    def test_delete_with_path_param(self):
        """ """
        r_final = CLIENT.delete_pet_r(petId=PET_ID)
        assert r_final == 200