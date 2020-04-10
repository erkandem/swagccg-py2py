[![Build Status](https://travis-ci.com/erkandem/swagccg-py2py.svg?token=EM8YQfR9wuLvQFQzBZ5o&branch=master)](https://travis-ci.com/erkandem/swagccg-py2py)
![](https://img.shields.io/badge/License-BSD-blue.svg)
![](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8%20-blue.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0181315639494eda8504e5b5092dee73)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=erkandem/swagccg-py2py&amp;utm_campaign=Badge_Grade)

# swagccg-py2py
*Swagger Client Code Generator. Using Python. For Python*

------------------------------------------

## Summary

Immediately testing new resources is important if resources are going to be 
co-dependent. While the tools at SwaggerHub are mind blowing 
they may represent an overkill for *not yet production* code.
Typing a single query can be done in any browser or with tools like curl.
This tool aims to place itself between those two categories.

On top of that, I would expect a programming language to be able to create its own tools. 
While Java is a mature and well established language, it might not be within 
the proficiency portfolio of each and everyone - not to mention the author.


## Get the Code
🚨 **not yet**
```bash
pip install swagccg-py2py
```

or clone it into your development environment

```bash
git clone https://github.com/erkandem/swagccg-py2py.git
```

or download the zip
```
https://github.com/erkandem/swagccg-py2py/archive/master.zip
```

## Getting started

The assumption here ist that you already have a ``swagger.json`` file.

The creation of a client comes down to:

```bash
python swagccg
```

If the ``config.json`` is not in your working directory
you would have to add its location to the call:
```bash
python -m swagccg -c /location/of/your/config.json
```

#### the configuration file

``config.json `` consists of two distinct parts. 
First, we would like to tell the script:
 - where we keep a swagger definition 
 - where we would like the client module to be created
 - what name we would like the client class to have

Since this is rather a development tool we would like 
to switch between target hosts with little afford (i.e. environment variable).
Therefore, we will offer it two targets which are later used to assamble
resource URLs.

We'll set a local (i.e. development) and remote (i.e. deployed) set of:
 - port
 - base url (i.e IPv4, host, domain_name.tld, subdomain.domain_name.tld)
 - scheme (http or https)

```json
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
```
## Client Creation 

```bash
python -m swagccg --c location/of/your/config.json
```


## Client Usage

Ultimately, the usage of the client depends on your requirements.
Nonetheless, the README would be incomplete without some usage examples:

```python
from auto_client import MyApiClient # default names - set them in confi.json
from settings import credential_dict # if needed

client_instance = MyApiClient('remote')  # or 'local' 
client_instance.login_with_api(credential_dict) 
data = client_instance.get_something_r() 
```

or

```python
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
```

## gotchas
 - authorization is highly custom
 - most of the swagger details are not parsed
 - models and mapping is omitted (``marshmallow``)
 - little to none ``HTTP status codes`` parsing
 - assumes knowledge on HTTP HEADER, BODY, METHOD
 - pass ``pass_through=True``  as parameter to receive the response object untouched

## recommended  reading
Mark Masse, REST API Design Rulebook - Designing Consistent RESTful Web Service Interfaces

[Petstore - API](http://petstore.swagger.io)

[OpenAPI Specififcation](https://github.com/OAI/OpenAPI-Specification)

## Contact

``Email`` [erkan.dem@pm.me](mailto:erkan.dem@pm.me)

``Issues``: [github.com/erkandem/swagccg-py2py/issues](https://github.com/erkandem/swagccg-py2py/issues)

``Source``: [github.com/erkandem/swagccg-py2py](https://github.com/erkandem/swagccg-py2py)

``Documentation``: [github.com/erkandem/swagccg-py2py/README.md](https://erkandem.github.io/swagccg-py2py)

## License
My project is licensed under terms of MIT.
For details please see the [``LICENSE``](LICENSE)

The examples and tests depend on the [petstore](http://petstore.swagger.io).
The attached petstore swagger by smartbear /  OpenAPI Initiative is licensed with MIT and is part of  the [Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html) licensed repo.

## Click Bait
Visitors who were interested in this repo also took a look at:

[swagccg-m2m - MatLab to MatLab Client Code Generation](https://github.com/erkandem/swagccg-m2m)

Because every programming language should be able to create its own tools.
