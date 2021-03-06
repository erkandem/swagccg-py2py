"""
The most important use case of the client is actually to query each
resource. However, this is co-dependent on the API server and is
a test for itself.

"""
import os
import json


class TestClientCreation(object):
    """ """
    client = None
    config_path = 'swagccg/tests/test_config.json'

    def test_client_creation(self):
        """
        test_client_creation
        items tested:
            - passing the commandline argument
            - reading the configuration file
            - reading the swagger file
            - writing the output
        """
        cmd = f'python -m swagccg  -c {self.config_path}'
        status = os.system(cmd)
        # response = subprocess.run(cmd, capture_output=True)
        # if response.returncode:
        #    print(response.stderr.decode('utf-8'))
        # assert response.returncode == 0
        assert status == 0

    def test_client_confi(self):
        """
        items tested:
            configuration file has the required keys
        """
        # cmd = 'python src/make_client.py --confi_path tests/test_confi.json'
        # status = os.system(cmd)
        with open(self.config_path) as f:
            config = json.load(f)
        config_keys_is = list(config)
        config_keys_should = [
            'swagger_path',
            'target_path',
            'class_name',
            'api_port_local',
            'api_url_base_local',
            'api_protocol_local',
            'api_port_remote',
            'api_url_base_remote',
            'api_protocol_remote'
        ]
        assert config_keys_is == config_keys_should

    def test_importing_test_client(self):
        import_succeeded = False
        from swagccg.tests.auto_client import MyClientClass
        self.client = MyClientClass()
        import_succeeded = True
        assert import_succeeded

    def test_import_from_template_1(self):
        import_succeeded = False
        from swagccg.src.client_template import client_imports_f
        import_succeeded = True
        assert import_succeeded

    def test_import_from_template_2(self):
        import_succeeded = False
        from swagccg.src.client_template import client_class_def_template_f
        import_succeeded = True
        assert import_succeeded

    def test_import_from_template_3(self):
        import_succeeded = False
        from swagccg.src.client_template import client_point_of_execution_f
        import_succeeded = True
        assert import_succeeded

    def test_import_from_template_4(self):
        import_succeeded = False
        from swagccg.src.client_template import client_method_template_f
        import_succeeded = True
        assert import_succeeded
