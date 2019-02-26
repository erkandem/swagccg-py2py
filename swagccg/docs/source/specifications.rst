Specifications
==================
What can you expect the client code to do and what not?

================ ======= ======== ======= ==========
**http Method**  ``GET`` ``POST`` ``PUT`` ``DELETE``
================ ======= ======== ======= ==========
**parameter in** -       -        -       -
query string     ✔️      ✔️       ✔️      ✔️
header           ✔️      ✔️       ✔️      ✔️
body             ⛔       ✔️       ✔️      ⛔
path             ✔️      ✔️       ✔️      ✔️
formData         ⛔       ☑️       ☑️      ☑️
================ ======= ======== ======= ==========

⛔ not specified by the RFC ✔️ supported ☑️ possible but cross your fingers


*Summary of the supported parameters and http-methods in this tool*

==== ========== ========== ========== ==========
\    Read       Write      Modify     Delete
==== ========== ========== ========== ==========
SQL  ``SELECT`` ``INSERT`` ``UPDATE`` ``DELETE``
HTTP ``GET``    ``POST``   ``PUT``    ``DELETE``
==== ========== ========== ========== ==========

*analogy between CRUD operations for SQL and RESTful Web API*


Query Strings
^^^^^^^^^^^^^^

Assign a dictionary to the ``fields_data`` argument to set the query
string. The key value pairs in the dictionary will be parsed to:

``endpoint``\ ➕\ ``?`` ➕ ``key=value&key2=value2``


path Parameters
^^^^^^^^^^^^^^^^^^^^^^^^

Path parameters will be dropped into the URL using a f-string. If you
require a specific format make sure you pass that path parameter as a
string.

This is because currently the data-type of the parameter which in
specified in swagger is not parsed .


Request Body
^^^^^^^^^^^^^^

By default any content in the body will be encoded in JSON and the
``Content-Type`` header will be set to ``application/json``.

There is no object validation built in.


Using formData in the Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you do need to use ``formData`` you can do so by adding the following header:

``Content-Type``: ``application/x-www-url-encoded``

This is the same as a query string but hidden in the body.


header
^^^^^^^^^^^^

There is no restriction on behalf of this tool on what you do with the
header. It is possible to send a custom header fields with any client
class method

Two headers are set by default:

``Content-Type`` : ``application/json``

``Accept`` : ``application/json``

Additionally any Authorization header will appended.

``Authorization`` : ``(Bearer) SomeFancyJwtTokenForExample``

References
^^^^^^^^^^^^

`CRUD <https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`__

`Overview of RESTful API Description_Languages <https://en.wikipedia.org/wiki/Overview_of_RESTful_API_Description_Languages>`__

`HTTP methods summary table <https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Summary_table>`__
