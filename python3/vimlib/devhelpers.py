#!/usr/bin/python3.4
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

# Copyright (C) 2014- The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
from importlib.util import find_spec

PYTHONBIN = os.environ.get("PYTHONBIN", sys.executable)
XTERM = os.environ.get("XTERM", "/usr/bin/urxvt -title Python -name Python -e")
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
            yield from flatten(val)
        else:
            yield val


def grep(patt, *args):
    """Filter iterables by regular expression."""
    regex = re.compile(patt)
    return filter(regex.search, flatten(args))


def run_command(cfstring, param):
    if not cfstring:
        print("No command string defined to run {}.".format(param),
              file=sys.stderr)
        return
    cmd = "{} {}".format(cfstring, param)
    print("running: {}".format(cmd))
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


def view(modname):
    """View the module, given by name as a string, in a file viewer."""
    filename = find_source_file(modname)
    if filename:
        ed = get_viewer()
        return run_command(ed, filename)
    else:
        print ("Could not find source to %s." % modname, file=sys.stderr)


def edit_import_line(importline):
    """Find the module referenced by the import source line and open in editor."""
    filename = find_source_file_from_import_line(importline)
    if filename:
        ed = get_editor()
        return run_command(ed, filename)
    else:
        print("Could not find source for {0}.".format(importline.strip()),
              file=sys.stderr)


def get_editor():
    return XEDITOR if "DISPLAY" in os.environ else EDITOR


def get_viewer():
    return XVIEWER if "DISPLAY" in os.environ else VIEWER


def find_source_file(modname, package=None):
    try:
        spec = find_spec(modname, package=package)
    except ValueError:
        return None
    if spec:
        if spec.has_location:
            return spec.origin
        else:
            print("Module source not found.", file=sys.stderr)
    else:
        print("Module not found.", file=sys.stderr)


def find_source_file_from_import_line(line):
    """Given a line of text that contains a form of import statement, return the
    package name.
    """
    line = line.strip()
    if line.startswith("import "):
        return find_source_file(line[7:].strip())
    elif line.startswith("from "):
        fromparts = line.split()
        return find_source_file("." + fromparts[3], fromparts[1])
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

