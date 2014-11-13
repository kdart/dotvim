#!/usr/bin/python
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

# Functions to make editing [X]HTML files in vim more productive.

# The following allows testing this module outside of a vim editor.
# The vimtest module is a mock of the internal vim module.

try:
    import vim
except ImportError:
    from ptest.vimlib import vimtest as vim


def get_encoding():
    # return current documents character encoding.
    return vim.eval("&fileencoding") or vim.eval("&encoding")

