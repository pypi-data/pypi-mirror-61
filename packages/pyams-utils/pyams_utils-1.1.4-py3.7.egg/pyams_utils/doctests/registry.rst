
Managing registry
-----------------

Pyramid provides a components registry, but this one is "hidden" and doesn't always have to be used
by Pyramid application developers.

In it's components model, PyAMS has made the choice to heavilly use the components registry to
register adapters and utilities!

And in addition to the "global" components registry, which is generally feed on application
startup, PyAMS defines a "local" registry, which allows to use components (generally persistent
utilities) which are stored into the ZODB!

So PyAMS provides custom functions which allows, for example, to look for utilities into the local
registry before looking into the global one; the local registry is generally set during request
traversing (when using PyAMS own traverser) by a subscriber to IBeforeTraverseEvent on any
object providing ISite:

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp()

    >>> from pyams_utils.registry import get_local_registry, set_local_registry
    >>> get_local_registry() is None
    True

Using a local registry requires a site:

    >>> from zope.site import LocalSiteManager
    >>> from zope.site.folder import Folder

    >>> root = Folder()
    >>> lsm = LocalSiteManager(root, default_folder=False)
    >>> root.setSiteManager(lsm)
    >>> root.getSiteManager() is lsm
    True

Let's now create a new request and handle traversing:

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyramid.events import NewRequest
    >>> from pyramid.threadlocal import manager
    >>> from pyams_utils.registry import handle_new_request, handle_site_before_traverse

    >>> request = DummyRequest(context=root)
    >>> handle_new_request(NewRequest(request))
    >>> get_local_registry() is None
    True
    >>> manager.push({'registry': config.registry, 'request': request})
    >>> handle_site_before_traverse(BeforeTraverseEvent(root, request))
    >>> get_local_registry() is lsm
    True

We can get the list of available registries:

    >>> from pyams_utils.registry import get_registries, get_global_registry, get_current_registry
    >>> list(get_registries())
    [<LocalSiteManager ++etc++site>, <Registry testing>]

We create a custom registry for testing, but while running into Pyramid the global registry is
always Zope's base components registry (so that direct interfaces adapters always work without
requiring the registry):

    >>> get_global_registry()
    <BaseGlobalComponents base>

The "current" registry is not the local registry: it's the last registry registered into
Pyramid's stack, or the global one if None:

    >>> get_current_registry()
    <Registry testing>

Let's now look for utilities; we will use a server timezone utility for this, which is defined
into PyAMS_utils package:

    >>> from zope.schema.vocabulary import getVocabularyRegistry
    >>> from pyams_utils.interfaces import TIMEZONES_VOCABULARY_NAME
    >>> from pyams_utils.timezone.vocabulary import TimezonesVocabulary
    >>> getVocabularyRegistry().register(TIMEZONES_VOCABULARY_NAME, TimezonesVocabulary)

    >>> from pyams_utils.interfaces.timezone import IServerTimezone
    >>> from pyams_utils.timezone.utility import ServerTimezoneUtility
    >>> tz = ServerTimezoneUtility()
    >>> tz.timezone
    'GMT'

We can register this utility into our local registry:

    >>> lsm['server_timezone'] = tz
    >>> lsm.registerUtility(tz, IServerTimezone, name='')

    >>> from pyams_utils.registry import registered_utilities, query_utility, get_utility, \
    ...                                  get_utilities_for, get_all_utilities_registered_for

    >>> list(registered_utilities())
    [UtilityRegistration(<LocalSiteManager ++etc++site>, IServerTimezone, '', server_timezone, None, ''), ...]
    >>> query_utility(IServerTimezone)
    <...ServerTimezoneUtility object at 0x...>
    >>> get_utility(IServerTimezone)
    <...ServerTimezoneUtility object at 0x...>
    >>> list(get_utilities_for(IServerTimezone))
    [('', <...ServerTimezoneUtility object at 0x...>)]
    >>> get_all_utilities_registered_for(IServerTimezone)
    [<...ServerTimezoneUtility object at 0x...>]

You can of course add several utilities for a same interface, as long as they are registered with
different names:

    >>> tz2 = ServerTimezoneUtility()
    >>> tz2.timezone = 'Europe/Paris'
    >>> lsm['tz2'] = tz2
    >>> lsm.registerUtility(tz2, IServerTimezone, name='tz2')

    >>> query_utility(IServerTimezone, name='tz2')
    <...ServerTimezoneUtility object at 0x...>
    >>> get_utility(IServerTimezone, name='tz2')
    <...ServerTimezoneUtility object at 0x...>
    >>> sorted(get_utilities_for(IServerTimezone))
    [('', <...ServerTimezoneUtility object at 0x...>), ('tz2', <...ServerTimezoneUtility object at 0x...>)]
    >>> get_all_utilities_registered_for(IServerTimezone)
    [<...ServerTimezoneUtility object at 0x...>, <...ServerTimezoneUtility object at 0x...>]

Tests cleanup:

    >>> manager.pop()
    {...}
    >>> set_local_registry(None)
    >>> tearDown()
