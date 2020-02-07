try:
    from .src import (
        client_point_of_execution_f,
        client_method_template_f,
        client_class_def_template_f,
        client_imports_f
    )
    from .src import (
        main,
        convert_to_snake_case,
        create_client_endpoints,
        seems_like_a_url
    )
except ImportError:
    from swagccg.src import (
        client_point_of_execution_f,
        client_method_template_f,
        client_class_def_template_f,
        client_imports_f
    )

    from swagccg.src import (
        main,
        convert_to_snake_case,
        create_client_endpoints,
        seems_like_a_url
    )
    print('Alternative import used')


