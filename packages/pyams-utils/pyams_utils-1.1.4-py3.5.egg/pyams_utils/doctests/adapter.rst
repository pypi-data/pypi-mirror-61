Managing adapters
=================

Adapters are components which are used to adapt a set of "input" objects instances, implementing
interfaces, to another object implementing another interface.

A lookup is done into components registry to find an available adapter for all these interfaces.

An adapter is nothing but a simple object; it doesn't have to inherit from anything, but it's
constructor must accept as many arguments as defined into adapter's "required" parameters length.

PyAMS_utils provides a small set of commonly used adapters:

  >>> from pyramid.testing import setUp, tearDown, DummyRequest
  >>> config = setUp()

  >>> from pyams_utils import includeme as include_utils
  >>> include_utils(config)

  >>> from pyams_utils import adapter

  >>> context, request, view = object(), object(), object()

  >>> context_adapter = adapter.ContextAdapter(context)
  >>> context_request_adapter = adapter.ContextRequestAdapter(context, request)
  >>> context_request_view_adapter = adapter.ContextRequestViewAdapter(context, request, view)

NullAdapter is a custom adapter which can be used to undefine an adapter in a given context:

  >>> null_adapter = adapter.NullAdapter(context, request)
  >>> null_adapter is None
  True


Annotations adapters
--------------------

Sometimes, some adapters have to store informations into one or more objects that they adapt
(generally the context); instead of using internal attributes which could conflict with properties
defined by other packages, we use annotations which are store in a custom "__annotations__" mapping
attribute; a custom factory is provided by PyAMS_utils to define and get such annotations:

  >>> from zope.interface import implementer, Interface
  >>> from zope.annotation.interfaces import IAttributeAnnotatable

  >>> class IMyContext(IAttributeAnnotatable):
  ...     """My context interface"""

  >>> @implementer(IMyContext)
  ... class MyContext:
  ...     """Context object class"""

  >>> class IMyAdapter(Interface):
  ...     """Adapter interface"""

  >>> @implementer(IMyAdapter)
  ... class MyAdapter:
  ...     """Adapter class"""
  ...     def __init__(self):
  ...         print("Creating adapter...")

  >>> def context_adapter_factory(context):
  ...     return adapter.get_annotation_adapter(context, "my.annotations.key", MyAdapter)

Adapter registration can be done using a decorator, but we register it manually for testing:

  >>> config.registry.registerAdapter(context_adapter_factory, (IMyContext,), IMyAdapter)

  >>> context = MyContext()
  >>> adapted = IMyAdapter(context)
  Creating adapter...
  >>> IMyAdapter.providedBy(adapted)
  True
  >>> 'my.annotations.key' in context.__annotations__
  True
  >>> context.__annotations__['my.annotations.key'] is adapted
  True

When calling the same adapter several times, the annotations lookup just returns the previously
created object:

  >>> IMyAdapter(context)
  <...MyAdapter object at 0x...>

The given "factory" argument value can be a factory or an interface; if an interface is provided,
a lookup is made for a registered factory for this interface:

  >>> from pyams_utils import factory
  >>> factory.register_factory(IMyAdapter, MyAdapter, registry=config.registry)

  >>> adapted = adapter.get_annotation_adapter(context, "my.annotations.key2", IMyAdapter,
  ...                                          registry=config.registry)
  Creating adapter...
  >>> context.__annotations__['my.annotations.key2'] is adapted
  True

If 'markers' argument is provided, this is a list of new interfaces that the new created object
will provide:

  >>> class IMyMarker1(Interface):
  ...     "First marker interface"

  >>> adapted = adapter.get_annotation_adapter(context, "my.annotations.key3", IMyAdapter,
  ...                                          markers=IMyMarker1, registry=config.registry)
  Creating adapter...
  >>> IMyMarker1.providedBy(adapted)
  True

By default, the context is set as parent of the new adapting object:

  >>> adapted.__parent__ is context
  True

If "parent" is set, this object will be defined as the parent instead of the context:

You can also define a callback which will be called after object creation:

  >>> adapted = adapter.get_annotation_adapter(context, "my.annotations.key4", IMyAdapter,
  ...                                          markers=IMyMarker1, registry=config.registry,
  ...                                          callback=lambda x: print('{!r}'.format(x)))
  Creating adapter...
  <...MyAdapter object at 0x...>


Tests cleanup:

  >>> tearDown()
