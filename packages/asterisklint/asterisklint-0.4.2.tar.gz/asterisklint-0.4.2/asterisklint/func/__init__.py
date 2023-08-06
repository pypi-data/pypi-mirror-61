# AsteriskLint -- an Asterisk PBX config syntax checker
# Copyright (C) 2015-2017  Walter Doekes, OSSO B.V.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from ..defines import ErrorDef, WarningDef


if 'we_dont_want_two_linefeeds_between_classdefs':  # for flake8
    class E_FUNC_BAD_ARGS(ErrorDef):
        message = "function {func!r} does not take these arguments '{data}'"

    class W_FUNC_BALANCE(WarningDef):
        message = ('function data {data!r} looks like unbalanced '
                   'parentheses/quotes/curlies')
