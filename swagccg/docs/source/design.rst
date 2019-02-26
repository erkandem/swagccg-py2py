Design
=======
Developers should be able to create code within the language they are using.
The tool was originally design to cover only GET requests with
a possibility for a  query string. The response was (and is) assumed to be
``JSON only``. But since the outwards facing parts are located in :func:`_do_call`,
:func:`_encode` and :func:`_decode` it's easy to add your logic.


Client Generation
----------------------

It is very easy to create client code because of triple-quoted strings and
*mustache like* option to drop in variables into the string. (**Python 3.6**)

Apart from file IO, the code generation can be boiled down to four steps
 - client imports
 - class definition and constructor
 - outwards facing request dispatching point
 - client methods

Imports
^^^^^^^^^^
The :func:`client_imports_f` can be used to define imports and as well as a module level comment.

Reference: :func:`src.client_template.client_imports_f`

Client Class Definition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Drop in the desired class name here.
Class and class-instance properties can be placed here.

Reference: :func:`src.client_template.client_class_def_template_f`

Point of Execution - POE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Well not really, since the POE only dispatches it to an external component.
Drop in your preferred way.

Reference: :func:`src.client_template.client_point_of_execution_f`


Client Class Encoding Decoding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, any request body will be encoded to json and
binary assuming utf-8 input.

Any response body will be decoded assuming JSON content.

On exception is if you want to encode ``formData``.
This is not handled on the client class level yet.
See :ref:`Specifications` for details.

Reference: :func:`src.client_template.client_encoding_decoding_point_f`

Client Class Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Each **http-method** will be rendered to one **client-class-method**
The name for the client-class-method  is derived from the ``operationId`` within swagger.
The actual name of the client-class-method will be http-method + the OperationId + ``_r``.

Each http-method has an operationId which may or may not include the http-method name.
If doesn't it will be attached.

Examples:

- A ``GET`` http-method on a ``getRessource`` OperationId would render to
  ``get_ressource_r``

- A ``GET`` http-method on a ``Ressource`` OperationId would also render to
  ``get_ressource_r``


Weak Point:

- A ``POST`` http-method on a ``getRessource`` OperationId would render to
  ``get_ressource_r`` because a


The parsing logic can be found within :func:`src.make_client.create_client_endpoints`

The client-class-method rendering logic is placed :func:`src.client_template.client_method_template_f`


