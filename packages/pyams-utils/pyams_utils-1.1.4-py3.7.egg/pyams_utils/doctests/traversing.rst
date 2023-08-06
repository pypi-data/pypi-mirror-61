
Traversing management
---------------------

Traversing is a common concept in web applications, which consists in going from parent to
child based on request elements.

For this to work, we have to now which is the parent of a given object, and this object have
to know which are it's childs.

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp()

    >>> from zope.interface import implementer, Interface, Attribute
    >>> class IMyFolder(Interface):
    ...     """Folder marker interface"""
    ...     value = Attribute("Test attribute")

    >>> from zope.container.folder import Folder
    >>> from zope.location import Location

    >>> @implementer(IMyFolder)
    ... class MyFolder(Folder):
    ...     """Custom location"""
    ...     name = ''
    ...     def __init__(self):
    ...         super(MyFolder, self).__init__()
    ...         self.value = object()

    >>> parent = MyFolder()
    >>> child = MyFolder()
    >>> parent['child'] = child
    >>> 'child' in parent
    True
    >>> child.__parent__ is parent
    True

    >>> from pyams_utils.traversing import get_name, get_parent
    >>> get_name(child)
    'child'

The "get_parent" function can be used to get parents of an object; by default, it returns any
object (including the context object itself) which implements an interface, or for which an
interface adapter is available:

    >>> get_parent(child) is child
    True

You can add a parameter to exclude context from search:

    >>> get_parent(child, allow_context=False) is parent
    True

You can also add a parameter to define a custom interface which searched object should implement,
or for which an adapter is available:

    >>> get_parent(child, IMyFolder, allow_context=False) is parent
    True

You can also set a condition, which is a function which may return True when applied on an object;
this condition is checked only if defined interface is implemented or adapted:

    >>> parent.name = 'Parent name'
    >>> get_parent(child, condition=lambda x: x.name.startswith('Parent')) is parent
    True

PyAMS provides a custom traverser called **NamespaceTraverser**; in addition to standard traverser
provided by Pyramid, this traverser allows to define custom "traversing namespaces", which can be
defined as adapters to *ITraversable* interface:

    >>> from pyramid.testing import DummyRequest
    >>> from pyams_utils.traversing import NamespaceTraverser

    >>> traverser = NamespaceTraverser(parent)
    >>> request = DummyRequest(path='/child/index.html', matchdict=None)
    >>> result = traverser(request)
    >>> result['root'] is parent
    True
    >>> result['virtual_root'] is parent
    True
    >>> result['virtual_root_path']
    ()
    >>> result['context'] is child
    True
    >>> result['view_name']
    'index.html'
    >>> result['traversed']
    ('child',)
    >>> result['subpath']
    ()

Let's try to add a sub-child:

    >>> subchild = MyFolder()
    >>> child['subchild'] = subchild

    >>> request = DummyRequest(path='/child/subchild/index.html', matchdict=None)
    >>> result = traverser(request)
    >>> result['root'] is parent
    True
    >>> result['virtual_root'] is parent
    True
    >>> result['virtual_root_path']
    ()
    >>> result['context'] is subchild
    True
    >>> result['view_name']
    'index.html'
    >>> result['traversed']
    ('child', 'subchild')
    >>> result['subpath']
    ()

Traversing namespaces are used by using a "++" in the URL, followed by the traversing adapter
name which should be used; the *traverse* method should return an object, which will be the base
of the following URL traversing; in some cases, some traversers can just update the initial
context or request, and return the initial context:

    >>> from pyams_utils.adapter import ContextAdapter
    >>> class TestTraverser(ContextAdapter):
    ...     def traverse(self, name, further=None):
    ...         return self.context.value

    >>> from zope.traversing.interfaces import ITraversable
    >>> config.registry.registerAdapter(TestTraverser, (IMyFolder,), ITraversable, name='test')

    >>> request = DummyRequest(path='/++test++/index.html', matchdict=None)
    >>> result = traverser(request)
    >>> result['root'] is parent
    True
    >>> result['virtual_root'] is parent
    True
    >>> result['virtual_root_path']
    ()
    >>> result['context'] is parent.value
    True
    >>> result['view_name']
    'index.html'
    >>> result['traversed']
    ('++test++',)
    >>> result['subpath']
    ()

Note here that the "name" argument is optional; if a value is present after the second "++"
character in the URL, it is this value that is given as parameter to the *traverse* method:

    >>> class AttrTraverser(ContextAdapter):
    ...     def traverse(self, name, further=None):
    ...         return getattr(self.context, name)

    >>> config.registry.registerAdapter(TestTraverser, (IMyFolder,), ITraversable, name='attr')

    >>> request = DummyRequest(path='/++attr++value/index.html', matchdict=None)
    >>> result = traverser(request)
    >>> result['root'] is parent
    True
    >>> result['virtual_root'] is parent
    True
    >>> result['virtual_root_path']
    ()
    >>> result['context'] is parent.value
    True
    >>> result['view_name']
    'index.html'
    >>> result['traversed']
    ('++attr++value',)
    >>> result['subpath']
    ()

Tests cleanup:

    >>> tearDown()
