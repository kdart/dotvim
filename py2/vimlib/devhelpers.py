#!/usr/bin/python2.7
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

"""Helper functions to aid Python development from interactive sessions and other tools.

Uses environment variables to set preferences. Below are the variables used and the
default values if not set.

EnvVar        Default
======        =======
PYTHONBIN     sys.executable
XTERM         rxvt -title Python -name Python -e
EDITOR        /usr/bin/vim
XEDITOR       /usr/bin/gvim
VIEWER        /usr/bin/view
XVIEWER       /usr/bin/gview

These are usually run from the Vim editor that has an embedded Python interpreter compiled in.
"""
import sys
import os
import re
import imp

PYTHONBIN = os.environ.get("PYTHONBIN", sys.executable)
#XTERM = os.environ.get("XTERM", "/usr/local/bin/urxvt -title Python -name Python -e")
XTERM = "/usr/local/bin/urxvt -title Python -name Python -e"
EDITOR = os.environ.get("EDITOR", "/usr/bin/vim")
VIEWER = os.environ.get("VIEWER", "/usr/bin/view")
XEDITOR = os.environ.get("XEDITOR", "/usr/bin/gvim")
XVIEWER = os.environ.get("XVIEWER", "/usr/bin/gview")


def flatten(alist):
    """Flatten a nested set of lists into one list, ignoring strings.

    Returns an iterator.
    """
    for val in alist:
        if isinstance(val, list):
            for val in flatten(val):
                yield val
        else:
            yield val


def grep(patt, *args):
    """Filter iterables by regular expression."""
    regex = re.compile(patt)
    return filter(regex.search, flatten(args))


def run_command(cfstring, param):
    if not cfstring:
        print ("No command string defined to run {}.".format(param), file=sys.stderr)
        return
    cmd = "{} {}".format(cfstring, param)
    return os.system(cmd)


def pyterm(name=None, interactive=1):
    """Run the module or file in another Python interpreter."""
    if name:
        cmd = python_command(name, interactive)
    else:
        cmd = "{} -i".format(PYTHONBIN)
    if "DISPLAY" in os.environ:
        return run_command(XTERM, cmd)
    else:
        return os.system(cmd)


def python_command(name, interactive=1):
    modname = module_from_path(name)
    if modname:
        return "{} {} -m '{}' ".format(PYTHONBIN, "-i" if interactive else "", modname)
    else:
        return "{} {} '{}' ".format(PYTHONBIN, "-i" if interactive else "", name)


def xterm(cmd="/bin/sh"):
    """Run the command in an external terminal, if possible, or the local terminal."""
    if "DISPLAY" in os.environ:
        return run_command(XTERM, cmd)
    else:
        return os.system(cmd)


def edit(modname):
    """Opens the module, given by name as a string, in an editor.  """
    filename = find_source_file(modname)
    if filename:
        ed = get_editor()
        return run_command(ed, filename)
    else:
        print ("Could not find source to {0}.".format(modname), file=sys.stderr)


def edit_module(mod):
    """Given a module object, open the source in an editor."""
    try:
        filename = mod.__file__
    except AttributeError:
        return
    if filename:
        ed = get_editor()
        return run_command(ed, filename)
    else:
        print("Could not find source to {}.".format(mod.__name__))


def edit_import_line(importline):
    """Find the module referenced by the import source line and open in editor."""
    filename = find_source_file_from_import_line(importline)
    if filename:
        ed = get_editor()
        return run_command(ed, filename)
    else:
        print ("Could not find source for {0}.".format(importline.strip()), file=sys.stderr)


def view(modname):
    """View the module, given by name as a string, in a file viewer."""
    filename = find_source_file(modname)
    if filename:
        ed = get_viewer()
        return run_command(ed, filename)
    else:
        print ("Could not find source to %s." % modname, file=sys.stderr)


def get_editor():
    return XEDITOR if "DISPLAY" in os.environ else EDITOR


def get_viewer():
    return XVIEWER if "DISPLAY" in os.environ else VIEWER


def exec_editor(*names):
    """Runs your configured editor on a supplied list of files.
    Uses exec, there is no return!
    """
    ed = get_editor()
    if ed.find("/") >= 0:
        os.execv(ed, (ed,)+names)
    else:
        os.execvp(ed, (ed,)+names)

def find_source_file(modname, path=None):
    if "." in modname:
        pkgname, modname = modname.rsplit(".", 1)
        pkg = find_package(pkgname)
        return find_source_file(modname, pkg.__path__)
    try:
        fo, fpath, (suffix, mode, mtype) = imp.find_module(modname, path)
    except ImportError:
        ex, val, tb = sys.exc_info()
        print("{} => {}: {}!".format(modname, ex.__name__, val), file=sys.stderr)
        return None
    if mtype == imp.PKG_DIRECTORY:
        fo, ipath, desc = imp.find_module("__init__", [fpath])
        fo.close()
        return ipath
    elif mtype == imp.PY_SOURCE:
        return fpath
    else:
        return None


def find_source_file_from_import_line(line):
    """Given a line of text that contains a form of import statement, return the package name."""
    line = line.strip()
    if line.startswith("import "):
        return find_source_file(line[7:].strip())
    elif line.startswith("from "):
        fromparts = line.split()
        return find_from_package(fromparts[1], fromparts[3])
    else:
        return None

def _iter_subpath(packagename):
    s = 0
    while True:
        i = packagename.find(".", s + 1)
        if i < 0:
            yield packagename
            break
        yield packagename[:i]
        s = i + 1


def _load_package(packagename, basename, searchpath):
    fo, _file, desc = imp.find_module(packagename, searchpath)
    if basename:
        fullname = "{}.{}".format(basename, packagename)
    else:
        fullname = packagename
    return imp.load_module(fullname, fo, _file, desc)


def find_package(packagename, searchpath=None):
    try:
        return sys.modules[packagename]
    except KeyError:
        pass
    for pkgname in _iter_subpath(packagename):
        if "." in pkgname:
            basepkg, subpkg = pkgname.rsplit(".", 1)
            pkg = sys.modules[basepkg]
            _load_package(subpkg, basepkg, pkg.__path__)
        else:
            try:
                sys.modules[pkgname]
            except KeyError:
                _load_package(pkgname, None, searchpath)
    return sys.modules[packagename]


def find_from_package(pkgname, modname):
    pkg = find_package(pkgname)
    try:
        fo, fpath, (suffix, mode, mtype) = imp.find_module(modname, pkg.__path__)
    except ImportError:
        ex, val, tb = sys.exc_info()
        print("{} => {}: {}!".format(modname, ex.__name__, val), file=sys.stderr)
        return None
    fo.close()
    if mtype == imp.PY_SOURCE:
        return fpath
    else:
        return None


def module_from_path(fname):
    """Find and return the module name given a full path name.
    Return None if file name not in the package path.
    """
    dirname, basename = os.path.split(fname)
    for p in sys.path:
        if fname.startswith(p):
            pkgname = ".".join(dirname[len(p)+1:].split("/"))
            if pkgname:
                return pkgname + "." + os.path.splitext(basename)[0]
            else:
                return os.path.splitext(basename)[0]
    return None

