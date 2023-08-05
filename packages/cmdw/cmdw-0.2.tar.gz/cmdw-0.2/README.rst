cmdw
==================

just get info of length and width of terminal/console/cmd


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    $ pip install cmd

cmdw supports Python 2 and newer, Python 3 and newer, and PyPy.

.. _pip: https://pip.pypa.io/en/stable/quickstart/


A Simple Example
----------------

What does it look like? Here is an example of a cmdw:

.. code-block:: python

    >>> import cmdw
    
    >>> cmdw.getWidth()
    >>> 164
    >>> cmdw.getHeight()
    >>> 26
    >>> cmdw.getWidth() * "#"
    >>> ############################################################################### 
    ....


Support
------

*   Python 2.7 +, Python 3.x
*   Windows, Linux

Links
-----

*   License: `BSD <https://github.com/licface/cmdw/blob/master/LICENSE.rst>`_
*   Code: https://github.com/licface/cmdw
*   Issue tracker: https://github.com/licface/cmdw/issues