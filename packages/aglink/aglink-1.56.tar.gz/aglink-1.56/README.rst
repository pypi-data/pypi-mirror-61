aglink
==================

Generator Links


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    $ pip install aglink

aglink supports Python 2 and newer, Python 3 and newer, and PyPy.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


Example
----------------

What does it look like? Here is an example of a simple generate link:

.. code-block:: batch

    $ agl.py -d --pcloud -p /root/Downloads "https://www110.zippyshare.com/v/0CtTucxG/file.html"


And what it looks like when run:

.. code-block:: batch

    $ GENERATE      : "http://srv-8.directserver.us/?file=473600c431"
      NAME          : "Game Of Thores S01E01.mp4"
      DOWNLOAD NAME : "Game Of Thores S01E01.mp4"

You can use on python interpreter

.. code-block:: python

    >>> from aglink.agl import autogeneratelink
    >>> c = autogeneratelink()
    >>> 
    >>> c.generate("https://www110.zippyshare.com/v/0CtTucxG/file.html", direct_download=True, download_path=".", pcloud = True, pcloud_username = "tester@gmail.com", pcloud_password = "tester123", wget = True, auto=True)
    >>> GENERATE      : "http://srv-8.directserver.us/?file=473600c431"
        NAME          : "Game Of Thores S01E01.mp4"
        DOWNLOAD NAME : "Game Of Thores S01E01.mp4"

For more options use '-h' or '--help'

.. code-block:: python

    $ aglink --help

    or 

    $ agl --help


Support
------

*   Direct Upload to Pcloud
*   Download With 'wget' (linux) or 'Internet Download Manager (IDM) (Windows) (pip install idm)'
*   Python 2.7 + (only)
*   Windows, Linux


Links
-----

*   License: `BSD <https://bitbucket.org/licface/aglink/src/default/LICENSE.rst>`_
*   Code: https://bitbucket.org/licface/aglink
*   Issue tracker: https://bitbucket.org/licface/aglink/issues