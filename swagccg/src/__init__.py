__version__ = '0.4.0'

from .client_template import (
    client_point_of_execution_f,
    client_method_template_f,
    client_class_def_template_f,
    client_imports_f
)

from .make_client import (
    main,
    convert_to_snake_case,
    create_client_endpoints,
    seems_like_a_url
)

