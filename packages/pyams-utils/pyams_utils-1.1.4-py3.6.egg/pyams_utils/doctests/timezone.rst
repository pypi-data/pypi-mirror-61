
Timezones management
--------------------

Datetimes are often quite hard to store and handle correctly when timezones are used.
A good approach is to store all datetimes in UTC, and to just display them using a correct
user's timezone.

PyAMS is proposing a server timezone utility, which allows to assign a static timezone to the
web application server; this "local" timezone is then used to render all datetimes.

Other extensions could provide a user's profile setting allowing any registered user to assign
a specific timezone to his own profile and display datetimes using this timezone; this should
require a custom adapter between :py:class:`IRequest <pyramid.interfaces.IRequest>` and
:py:class:`ITZInfo <zope.interface.common.idatetime.ITZInfo>` to handle this specification.
Other systems can also get timezone from source IP address (see, for example,
`https://ip-api.com/').

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp()

    >>> from pyams_utils import includeme
    >>> includeme(config)

    >>> request = DummyRequest()
    >>> from zope.interface.common.idatetime import ITZInfo
    >>> ITZInfo(request)
    <StaticTzInfo 'GMT'>

    >>> from datetime import datetime
    >>> from pyams_utils.timezone import tztime, gmtime, localgmtime

    >>> now = datetime.utcnow()
    >>> now.tzinfo is None
    True
    >>> tztime(now)
    datetime.datetime(..., tzinfo=<StaticTzInfo 'GMT'>)

    >>> from pyams_utils.interfaces.timezone import IServerTimezone
    >>> from pyams_utils.timezone.utility import ServerTimezoneUtility
    >>> tz = ServerTimezoneUtility()
    >>> tz.timezone = 'Europe/Paris'
    >>> tz.timezone
    'Europe/Paris'

    >>> config.registry.registerUtility(tz, IServerTimezone, name='')
    >>> from pyams_utils.registry import query_utility
    >>> stz = query_utility(IServerTimezone)
    >>> stz
    <...ServerTimezoneUtility object at 0x...>
    >>> stz.timezone
    'Europe/Paris'
    >>> stz is tz
    True

    >>> ITZInfo(request)
    <DstTzInfo 'Europe/Paris' ... STD>

    >>> tznow = tztime(now)
    >>> tznow
    datetime.datetime(..., tzinfo=<DstTzInfo 'Europe/Paris' ... STD>)
    >>> gmtime(tznow)
    datetime.datetime(..., tzinfo=<StaticTzInfo 'GMT'>)
    >>> localgmtime(tznow)
    datetime.datetime(..., tzinfo=<StaticTzInfo 'GMT'>)

Tests cleanup:

    >>> tearDown()
