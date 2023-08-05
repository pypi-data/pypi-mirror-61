# Hydrus API
Python module implementing the Hydrus API.

# Requirements
- Python 3
- requests library (`pip install requests`)

# Installation
`$ pip install hydrus-api`

If you want to use the package in your own (installable) Python project, specify
it in your `setup.py` using: `install_requires=['hydrus-api']`.

# Description
It is _highly_ recommended that you do not solely rely on the docstrings in this
module to use the API, instead read the official documentation (latest
[here](https://hydrusnetwork.github.io/hydrus/help/client_api.html)).

When instantiating `Client` the `acccess_key` is optional, allowing you to
initially manually request permissions using `request_new_permissions()`.
Alternatively there is `utils.request_api_key()` to make this easier. You can
instantiate a new `Client` with the returned access key after that.

If the API version the module is developed against and the API version at the
specified endpoint differ, you will be warned but not prevented from using any
functionality -- this might have unintended consequences, be careful.

If something with the API goes wrong, a subclass of `APIError`
(`MissingParameter`, `InsufficientAccess`, `ServerError`) or `APIError` itself
will be raised with the [`requests.Response`](http://docs.python-requests.org/en/master/api/#requests.Response)
object that caused the error. `APIError` will only be raised directly, if the
returned status code is unrecognized.

The module provides `Permission`, `URLType`, `ImportStatus`, `TagAction`,
`TagStatus` and `PageType` enums for your convenience. Values in the response
data, represented by the enums, are automatically converted -- this makes them
more easily readable, the enum values can still be handled like regular
integers. Some utility functions are available in `hydrus.utils`.

Check out `examples/` for some example applications.
