Cloudfiles-light
================

Lightweight helper for using rackspace cloudfiles. Has way fewer dependencies (and features) than the official sdk `pyrax <https://github.com/pycontribs/pyrax>`_

Usage
=====

::

    from cloudfiles_light import CloudFilesSession

    session = CloudFilesSession(username, apikey, region)
    # list files
    session.get('my-container')

``session`` is a `requests <http://docs.python-requests.org/en/master/>`_ session that prepends the endpoint base url and handles authentication (requests and refreshes tokens and adds as headers)

This is aimed at using the `Rackspace Cloud Files API 1.0 <https://developer.rackspace.com/docs/cloud-files/v1/>`_

License
=======

MIT
