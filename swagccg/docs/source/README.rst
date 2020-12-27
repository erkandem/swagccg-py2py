|Build Status| |image1| |image2| |Codacy Badge| |image4|

swagccg-py2py
=============

*Swagger Client Code Generator. Using Python. For Python*

--------------

Summary
-------

There is a) professional SDK generation tools (OpenAPI code gen and
others) and b) tools like postman or simply ``curl`` This tool aims to
place itself a notch more useful than querying your API with ``curl``.

Fork it and use it as a template.

Get the Code
------------

.. code:: bash

   pip install swagccg-py2py

or clone it into your development environment

.. code:: bash

   git clone https://github.com/erkandem/swagccg-py2py.git

or download the zip

::

   https://github.com/erkandem/swagccg-py2py/archive/master.zip

Getting started
---------------

The assumption here ist that you already have a ``swagger.json`` file.

The creation of a client comes down to:

.. code:: bash

   python swagccg

If the ``config.json`` is not in your working directory you would have
to add its location to the call:

.. code:: bash

   python -m swagccg -c /location/of/your/config.json

the configuration file
^^^^^^^^^^^^^^^^^^^^^^

``config.json`` consists of two distinct parts. First, we would like to
tell the script: - where we keep a swagger definition - where we would
like the client module to be created - what name we would like the
client class to have

Since this is rather a development tool we would like to switch between
target hosts with little afford (i.e. environment variable). Therefore,
we will offer it two targets which are later used to assamble resource
URLs.

We’ll set a local (i.e. development) and remote (i.e. deployed) set of:
- port - base url (i.e IPv4, host, domain_name.tld,
subdomain.domain_name.tld) - scheme (http or https)

.. code:: json

   {
     "swagger_path": "/home/abuser/apiclient/swagger.json",
     "target_path": "/home/abuser/apiclient/auto_client.py",
     "class_name": "Myclient",


     "api_port_local": "5000",
     "api_url_base_local": "127.0.0.1",
     "api_protocol_local": "http",

     "api_port_remote": "80",
     "api_url_base_remote": "deployed.com",
     "api_protocol_remote": "https"
   }

Client Creation
---------------

.. code:: bash

   python -m swagccg --c location/of/your/config.json

Client Usage
------------

Ultimately, the usage of the client depends on your requirements.
Nonetheless, the README would be incomplete without some usage examples:

.. code:: python

   from auto_client import MyApiClient # default names - set them in confi.json
   from settings import credential_dict # if needed

   client_instance = MyApiClient('remote')  # or 'local' 
   client_instance.login_with_api(credential_dict) 
   data = client_instance.get_something_r() 

or

.. code:: python

   import os
   from pathlib import Path
   from dotenv import load_dotenv
   from auto_client import MyApiClient
   #%%
   env_path = Path('.') / '.env'
   load_dotenv(dotenv_path=env_path)
   client_instance = MyApiClient('remote')

   #%% login of course depends on the server
   client_instance.login_with_api({
       'username': os.getenv('API_USERNAME'),
       'password': os.getenv('API_PASSWORD')
   })
   param_dict = dict(name='value')
   data = client_instance.get_something_r(fields_data=param_dict)

gotchas
-------

-  authorization is highly custom
-  most of the swagger details are not parsed
-  models and mapping is omitted (``marshmallow``)
-  little to none ``HTTP status codes`` parsing
-  assumes knowledge on HTTP

recommended reading
-------------------

Mark Masse, REST API Design Rulebook - Designing Consistent RESTful Web
Service Interfaces

`Petstore - API <http://petstore.swagger.io>`__

`OpenAPI
Specififcation <https://github.com/OAI/OpenAPI-Specification>`__

Contact
-------

``Email`` erkan.dem@pm.me

``Issues``:
`github.com/erkandem/swagccg-py2py/issues <https://github.com/erkandem/swagccg-py2py/issues>`__

``Source``:
`github.com/erkandem/swagccg-py2py <https://github.com/erkandem/swagccg-py2py>`__

``Documentation``:
`github.com/erkandem/swagccg-py2py/README.md <https://erkandem.github.io/swagccg-py2py>`__

License
-------

My project is licensed under terms of MIT. For details please see the
```LICENSE`` <LICENSE>`__

The examples and tests depend on the
`petstore <http://petstore.swagger.io>`__. The attached petstore swagger
by smartbear / OpenAPI Initiative is licensed with MIT and is part of
the `Apache 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`__
licensed repo.

Click Bait
----------

Visitors who were interested in this repo also took a look at:

`swagccg-m2m - MatLab to MatLab Client Code
Generation <https://github.com/erkandem/swagccg-m2m>`__

Because every programming language should be able to create its own
tools.

change log
----------

v0.4.0 2020-27-20
~~~~~~~~~~~~~~~~~

**breaking**

-  remove “logic” around trying to load response content just return the
   fluffing response

-  completely remove refreshing related stuff

-  add typing where ease and added indentation for arguments (too long)

.. |Build Status| image:: https://travis-ci.com/erkandem/swagccg-py2py.svg?token=EM8YQfR9wuLvQFQzBZ5o&branch=master
   :target: https://travis-ci.com/erkandem/swagccg-py2py
.. |image1| image:: https://img.shields.io/badge/License-BSD-blue.svg
.. |image2| image:: https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8%20-blue.svg
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/0181315639494eda8504e5b5092dee73
   :target: https://www.codacy.com?utm_source=github.com&utm_medium=referral&utm_content=erkandem/swagccg-py2py&utm_campaign=Badge_Grade
.. |image4| image:: https://img.shields.io/pypi/v/swagccg?color=blue
