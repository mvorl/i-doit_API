Abstract
========

This is a (not yet complete) Python implementation of Benjamin Heisig's excellent PHP-based `i-doit API client library <https://github.com/i-doit/i-doit-api-client-php>`_ (version 0.10).
It was originally based on `DinoTools' wrapper to access the i-doit API <https://github.com/DinoTools/python-idoit>`_ but has since outgrown it.

As this implementation doesn't use curl for the communication, it does not support all features of the PHP client library, e.g. proxy support.

The API's documentation (apart from the methods' documentation in this package - which was largely copied from the PHP code) is available in the `Synetics knowledge base <https://kb.i-doit.com/pages/viewpage.action?pageId=7831613>`_.

Testing
=======

To perform API tests, the test scripts connect to the `i-doit Demo system <https://demo.i-doit.com>`_. For this to work, the correct JSON-RPC API key needs to be entered in the file `idoitapi/tests/.config`.
It can be retrieved from the i-doit demo system by logging in, opening the user menu by hovering over the user name, choosing 'Administration', and clicking on 'Interfaces / External data`, 'JSON-RPC API', and 'Common Settings'.


ToDo
====

* implement more tests - this whole package is in daily use, but has only seen cursory testing so far!
* implement requests for API namespace 'checkmk.statictag' (idoitapi/CheckMKStaticTag.py)
* implement requests for API namespace 'checkmk.tags' (idoitapi/CheckMKTags.py)
* implement requests for API namespace 'monitoring.livestatus' (idoitapi/MonitoringLivestatus.py)
