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

"""
Mock vim module used for testing vimlib outside of vim itself.
This module mocks just enough of the vim module to import vimlib
without errors.
"""

class error(Exception):
    pass


class Window:
    pass


class Current:
    pass


class Range:
    pass


class Buffer(bytearray):
    pass


def command(s):
    print("vim command:", s)


# Buffer mock
buffers = [Buffer()]
buffers[0].name = "<unknown>"

# Window mock
windows = [Window()]

# Current object mock
current = Current()
current.window = windows[0]
current.buffer = buffers[0]
current.line = ""
current.range = Range()

