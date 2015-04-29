import sys


def exit(msg):
    """
    Exit execution, print ``msg`` to stdout and exit.
    This function currently makes use of `sys.exit`_, which raises
    `SystemExit`_. Therefore, it's possible to detect and recover from inner
    calls to `exit` by using ``except SystemExit`` or similar.
    .. _sys.exit: http://docs.python.org/library/sys.html#sys.exit
    .. _SystemExit: http://docs.python.org/library/exceptions.html#exceptions.SystemExit
    """
    sys.exit(msg)