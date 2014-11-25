#!/usr/bin/python2.7
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab


"""
Vim module for editing CSS.
"""

try:
    import vim
except ImportError:
    # for running outside of vim when testing
    from vimlib2 import vimtest as vim

