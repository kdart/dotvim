#!/usr/bin/python2.7
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""Vim editor extensions for Python.

For Vim users. Not an essential part of the framework, but helps developing Python
code (including test cases) with Vim.

This module is intended to run in the Vim editor that has a built-in Python
interpreter. It provides additional functionality to vim in general, but also some
functions designed specifically for editing other python source files.

Currently this requires custom compiling Vim with python3 support.
"""

try:
    import vim
except ImportError:
    # for testing this module outside of vim
    from . import vimtest as vim


import sys, os
import re
import ast
import pprint

from . import devhelpers

pyterm = devhelpers.pyterm
xterm = devhelpers.xterm

EXECTEMP = "/var/tmp/python_vim_temp_%s.py" % (os.getpid())

re_class_export = re.compile(r"^class ([A-Z][a-zA-Z0-9_]*)")
re_def_export = re.compile(r"^def ([a-zA-Z][a-zA-Z0-9_]*)")


def normal(str):
    vim.command("normal "+str)


def test_count():
    print (int(vim.eval("v:count")))


def str_range(vrange):
    return "\n".join(vrange) + "\n"


def exec_vimrange_in_term(vrange):
    tf = open(EXECTEMP , "w")
    tf.write(str_range(vrange))
    tf.close()
    devhelpers.run_command(devhelpers.XTERM, "{} -i {}".format(devhelpers.PYTHONBIN, EXECTEMP))


def insert_viminfo():
    """Insert a vim line with tabbing related settings reflecting current settings."""
    # The following line is to prevent this vim from interpreting this as a real
    # v-i-m tagline.
    vi = ["# %s" % ("".join(['v','i','m']),)]
    for var in ('ts', 'sw', 'softtabstop'):
        vi.append("%s=%s" % (var, vim.eval("&%s" % (var,))))
    for var in ('smarttab', 'expandtab'):
        if int(vim.eval("&%s" % var)):
            vi.append(var)
    if vim.eval("&ft") != "python":
        vi.append("ft=python")
    vim.current.range.append(":".join(vi))

def insert__all__():
    path, name = os.path.split(vim.current.buffer.name)
    if name == "__init__.py":
        insert__all__pkg(path)
    else:
        insert__all__mod()

def insert__all__mod():
    classes = []
    funcs = []
    for line in vim.current.buffer:
        mo = re_class_export.search(line)
        if mo:
            classes.append(mo.group(1))
        mo = re_def_export.search(line)
        if mo:
            funcs.append(mo.group(1))
    vim.current.range.append("__all__ = [%s]" % (", ".join(map(repr, classes+funcs))))

def insert__all__pkg(path):
    files = devhelpers.grep("^[A-Za-z]+\\.py$", os.listdir(path))
    res = []
    for name, ext in map(os.path.splitext, files):
        res.append(name)
    vim.current.range.append("__all__ = [%s]" % (", ".join(map(repr, res))))


# utility functions

def keyword_edit():
    devhelpers.edit(vim.eval('expand("<cword>")'))


def import_edit():
    devhelpers.edit_import_line(vim.current.line)


def keyword_view():
    devhelpers.view(vim.eval('expand("<cword>")'))


def keyword_split():
    modname = vim.eval('expand("<cword>")')
    filename = devhelpers.find_source_file(modname)
    if filename is not None:
        vim.command("split %s" % (filename,))
    else:
        print("Could not find source to %s." % modname, file=sys.stderr)


def visual_edit():
    text = get_visual_selection()
    if "\n" in text:
        print("bad selection")
    else:
        devhelpers.edit(text)


def visual_view():
    text = get_visual_selection()
    if "\n" in text:
        print("bad selection")
    else:
        devhelpers.view(text)


def get_visual_selection():
    b = vim.current.buffer
    start_row, start_col = b.mark("<")
    end_row, end_col = b.mark(">")
    if start_row == end_row:
        return b[start_row-1][start_col:end_col+1]
    else:
        s = [b[start_row-1][start_col:]]
        for l in b[start_row:end_row-2]:
            s.append(l)
        s.append(b[end_row-1][:end_col+1])
        return "\n".join(s)


def prettify():
    """Evaluate source lines in buffer, replace the lines with a pretty-printed representation."""
    orig = get_visual_selection()
    if not orig:
        print("No selection.")
        return
    b = vim.current.buffer
    obj = ast.literal_eval(orig)
    newstr = pprint.pformat(obj, indent=4, width=100)
    start_row, start_col = b.mark("<")
    end_row, end_col = b.mark(">")
    b[start_row-1:end_row] = newstr.split("\n")

