
Managing requests
-----------------

PyAMS_utils package provides some useful functions to handle requests.

The "check_request" function can be used when you have to be sure that a request is active in
the current execution thread; if no "real" request is active, a new one is created:

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp()

    >>> from pyams_utils.request import PyAMSRequest, query_request, check_request
    >>> request = query_request()
    >>> request is None
    True
    >>> request = check_request()
    >>> request
    <PyAMSRequest at ... GET http://localhost/>

If a new request is created "from scratch", it's registry is assigned to global registry:

    >>> request.registry
    <Registry testing>

A request context can be used to activate a request into execution thread:

    >>> from pyramid.threadlocal import RequestContext
    >>> with RequestContext(request) as context_request:
    ...     context_request is request
    True
    >>> with RequestContext(request):
    ...     context_request = check_request()
    ...     context_request is request
    True

Requests can now support annotations to set and retrieve any information to a given request:

    >>> from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
    >>> from zope.annotation.attribute import AttributeAnnotations
    >>> from pyams_utils.registry import get_global_registry
    >>> config.registry.registerAdapter(AttributeAnnotations, (IAttributeAnnotatable, ), IAnnotations)

    >>> from pyams_utils.request import get_request_data, set_request_data
    >>> set_request_data(request, 'test', 'This is request data')
    >>> get_request_data(request, 'test')
    'This is request data'

Annotations can be used to automatically reify a given property into request annotations:

    >>> from pyams_utils.request import request_property
    >>> class RequestPropertyTestClass(object):
    ...
    ...     @request_property(key='My property')
    ...     def my_property(self):
    ...         print("This is my property")
    ...         return 1
    ...
    >>> with RequestContext(request):
    ...     instance = RequestPropertyTestClass()
    ...     instance.my_property()
    This is my property
    1

As property value is cached into request annotations, other property calls will just return
cached value:

    >>> with RequestContext(request):
    ...     instance.my_property()
    1

The "copy_request" function  is used to clone another request. All request methods and properties
defined via "add_request_method()" are kept, as "registry" and "root" attributes:

    >>> from pyams_utils.request import copy_request
    >>> request2 = copy_request(request)
    >>> request2.registry is request.registry
    True
    >>> request2.root is None
    True

Tests cleanup:

    >>> tearDown()
