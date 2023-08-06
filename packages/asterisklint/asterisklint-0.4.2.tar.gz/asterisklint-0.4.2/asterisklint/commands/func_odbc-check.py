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
"""
Do sanity checks on func_odbc.conf. Takes 'func_odbc.conf' as argument.
Suppress errors using ALINT_IGNORE env.
"""
from asterisklint import FileFuncOdbcParser
from asterisklint.defines import MessageDefManager
from asterisklint.mainutil import MainBase


class Main(MainBase):
    def create_argparser(self, argparser_class):
        parser = argparser_class(
            description=(
                'Do sanity checks on func_odbc.conf. Suppress comma separated '
                'error classes through the ALINT_IGNORE environment variable. '
                'Returns 1 if any issue was reported.'))
        parser.add_argument(
            'func_odbc', metavar='FUNC_ODBC_CONF', nargs='?',
            default='./func_odbc.conf',
            help="path to func_odbc.conf")
        return parser

    def handle_args(self, args):
        parser = FileFuncOdbcParser()
        parser.include(args.func_odbc)
        for func_odbc_context in parser:
            pass

        # MessageDefManager.raised is a dict of messages ordered by
        # message type. All message types share the same muted flag,
        # so we need only examine the first.
        if any(not i[0].muted for i in MessageDefManager.raised.values()):
            return 1


main = Main()
