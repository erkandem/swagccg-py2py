import re
import json
import argparse
from urllib.parse import urlparse
from urllib.request import urlopen
try:
    from swagccg.src.client_template import client_imports_f
    from swagccg.src.client_template import client_class_def_template_f
    from swagccg.src.client_template import client_method_template_f
    from swagccg.src.client_template import client_point_of_execution_f
    from swagccg.src.client_template import client_encode_decoding_point_f
    from swagccg.src.client_template import dir_template_f
except ImportError:
    from .client_template import client_imports_f
    from .client_template import client_class_def_template_f
    from .client_template import client_method_template_f
    from .client_template import client_point_of_execution_f
    from .client_template import client_encoding_decoding_point_f
    from .client_template import dir_template_f
    print("Alternative import used.")

PARSED_HTTP_METHODS = ['GET', 'POST', 'DELETE', 'PATCH', 'PUT']


def convert_to_snake_case(name: str) -> str:
    """via https://stackoverflow.com/a/1176023 """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def create_client_endpoints(swagger_data, api_paths):
    methods_list = []
    method_names = []
    n = 0
    for api_path in api_paths:
        # compose the method name
        http_methods = list(swagger_data['paths'][api_path])

        for http_method in http_methods:
            operation = f'initial_{n}'
            n += 1
            doc_string = f' '
            if 'operationId' in swagger_data['paths'][api_path][http_method]:
                operation = swagger_data['paths'][api_path][http_method]['operationId']
            if 'summary' in swagger_data['paths'][api_path][http_method]:
                doc_string = swagger_data['paths'][api_path][http_method]['summary']

            # convert to snake case if it isn't already
            operation = convert_to_snake_case(operation)

            # check if the HTTP verb is already part of the operation name
            scan = [re.match(verb, operation, flags=re.IGNORECASE) is None for verb in PARSED_HTTP_METHODS]
            if len(scan) == sum(scan):
                method_name = f'{http_method}_{operation}_r'.lower()
            else:
                method_name = f'{operation}_r'.lower()
            method_name = method_name.replace('-', '_')
            method_names.append(method_name)
            # handle path parameters explicitly as opposed to parameters within the query string
            path_params = ''
            if 'parameters' in swagger_data['paths'][api_path][http_method]:
                parameters = swagger_data['paths'][api_path][http_method]['parameters']
                for p in parameters:
                    if p['in'] == 'path':
                        path_params += f', {p["name"]}'

            methods_list.append(
                client_method_template_f(
                    method_name=method_name,
                    http_verb=http_method,
                    api_path=api_path,
                    doc_string=doc_string,
                    path_params=path_params
                )
            )
    client_methods = ''
    for i in range(len(methods_list)):
        client_methods = client_methods + methods_list[i]
    return client_methods, method_names


def seems_like_a_url(url):
    """ is_url https://stackoverflow.com/a/52455972/10124294 """
    try:
        r = urlparse(url)
        return all([r.scheme, r.netloc, r.path])
    except ValueError:
        return False


def main(config_path=None):
    """ control flow """
    if config_path is None:
        config_path = 'config.json'
    if config_path is None:
        config_path = '/tmp/auto_client.py'
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        msg = (f'Could not find a configuration file at: '
               f'\n{config_path}\n '
               f'Did you pass a path to the location of the configuration file?'
               f'The default assumption search only the working directory.'
               f'If yes, try to pass an absolute path.')
        raise FileNotFoundError(msg)

    try:
        if seems_like_a_url(config['swagger_path']):
            with urlopen(config['swagger_path']) as url:
                swagger_data = json.loads(url.read().decode())
        else:
            with open(config['swagger_path'], 'r') as f:
                swagger_data = json.load(f)
    except FileNotFoundError:
        msg = (f'Could not find the swagger specification file at:\n'
               f'{config["swagger_path"]}\n'
               f'A look inside {config_path} is worth a shot.')
        raise FileNotFoundError(msg)

    if 'basePath' in swagger_data:
        config['basePath'] = swagger_data['basePath']
    else:
        config['basePath'] = ''
        Warning(f"``basePath`` does not seem to be assigned within:\n"
                f"{config['swagger_path']}\n"
                f"Did not result in any data. This isn't necessarily a problem\n"
                f"Setting ``basePath`` as '' (empty string)")

    if 'paths' in swagger_data:
        api_paths = list(swagger_data['paths'])
    else:
        raise ValueError(f"The swagger definition below did not provide any ``paths``:\n"
                         f"{config['swagger_path']}\n"
                         f"An API definition without paths? Test? Exiting.")

    client_imports = client_imports_f()
    client_class_def = client_class_def_template_f(args=config)
    client_encode_decoding_point = client_encoding_decoding_point_f()
    client_point_of_execution = client_point_of_execution_f()

    client_methods, method_names = create_client_endpoints(
        api_paths=api_paths,
        swagger_data=swagger_data
    )
    client_dir_function_str = dir_template_f(method_names)
    client_class_def = client_class_def.replace('\n    # def __dir__(self):\n', client_dir_function_str, 1)
    all_in_one = (
            client_imports
            + client_class_def
            + client_point_of_execution
            + client_encode_decoding_point
            + client_methods[:-4]  # remove the last 4 white spaces / indentation#
    )
    try:
        with open(config['target_path'], 'wb') as f:
            f.write(all_in_one.encode('utf-8'))

        msg = (f"Done! The client was created at:\n\n{config['target_path']}\n"
               f"Next step is to customize your client and test it with some sample requests.\n")
        print(msg)
    except IOError:
        raise IOError(f'Could not write at the desired location at:\n'
                      f'{config["target_path"]}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-path', '-c', action='store', default='config.json')
    args = parser.parse_args()
    main(config_path=args.config_path)
