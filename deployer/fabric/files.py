"""
Module providing easy API for working with files.
"""

import re

from fabric.utils import abort


def copy_template(filename, destination, context=None, use_extended=True):
    """Render and copy a local template text file to local destination

    If use_
    """
    text = None
    with open(filename, 'r') as input:
        text = input.read()
    if context:
        if use_extended:
            def replacer(matchobj):
                try:
                    ctx = context if matchobj.group('ns') is None else context[matchobj.group('ns')]
                    return ctx[matchobj.group('name')]
                except:
                    abort('Cannot find definition for variable %s' % matchobj.group())
                    print "oops "
            text = re.sub(r'(?<!\$)\$\{(?:(?P<ns>\w+):)?(?P<name>\w+)\}', replacer, text)
        else:
            text = text % context
    with open(destination, 'w') as output:
        output.write(text)