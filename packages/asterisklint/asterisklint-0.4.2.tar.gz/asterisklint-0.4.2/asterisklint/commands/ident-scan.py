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
Report similarly named contexts, labels and variables. Takes
'extensions.conf' as argument. All parse errors are suppressed.
"""
from collections import defaultdict

from asterisklint import FileDialplanParser
from asterisklint.defines import MessageDefManager
from asterisklint.varfun import VarLoader
from asterisklint.mainutil import MainBase

try:
    import editdistance  # https://pypi.python.org/pypi/editdistance
except ImportError:
    editdistance = None


class Main(MainBase):
    def create_argparser(self, argparser_class):
        parser = argparser_class(
            description=(
                'Report similarly named contexts, labels and variables. '
                'All parse errors are suppressed. Returns 1 if any potential '
                'issue was reported.'))
        parser.add_argument(
            '-v', '--verbose', action='store_true',
            help='list all identifiers first before reporting similarities')
        parser.add_argument(
            'dialplan', metavar='EXTENSIONS_CONF', nargs='?',
            default='./extensions.conf',
            help='path to extensions.conf')
        return parser

    def handle_args(self, args):
        MessageDefManager.muted = True

        loader = VarLoader()
        parser = FileDialplanParser()
        parser.include(args.dialplan)
        dialplan = next(iter(parser))

        contexts_by_name = list(sorted(
            (context.name for context in dialplan.contexts),
            key=(lambda x: x.lower())))
        # TODO: dialplan.all_labels is not a public interface..
        labels_by_name = list(sorted(
            dialplan.all_labels, key=(lambda x: x.lower())))
        # TODO: loader._variables is *not* a public interface..
        varlist_by_name = list(sorted(
            loader._variables.items(), key=(lambda x: x[0].lower())))

        if args.verbose:
            self.print_contexts(contexts_by_name)
            self.print_labels(labels_by_name)
            self.print_variables(varlist_by_name)

        # Calculate Levenshtein distance if available. Complain if
        # module wasn't loaded and the user did not ask for verbose
        # printing either.
        if editdistance:
            identifiers = (
                set(contexts_by_name) |
                set(labels_by_name) |
                set([i[0] for i in varlist_by_name]))
            ret = self.print_distance(identifiers)
        elif args.verbose:
            ret = 0
        else:
            raise ImportError(
                'Loading editdistance failed. Using this command without '
                'the editdistance and without verbose mode is a no-op.')

        return ret

    def print_contexts(self, contexts_by_name):
        print('Contexts encountered:')
        for context in contexts_by_name:
            print('  {}'.format(context))
        print()

    def print_labels(self, labels_by_name):
        print('Labels encountered:')
        for label in labels_by_name:
            print('  {}'.format(label))
        print()

    def print_variables(self, varlist_by_name):
        print('Variables encountered:')
        for variable, occurrences in varlist_by_name:
            print('  {:32}  [{} times in {} files]'.format(
                variable, len(occurrences),
                len(set(i.filename for i in occurrences))))
        print()

    def print_distance(self, identifiers):
        id_by_name = sorted(
            identifiers, key=(lambda x: x.lower()))
        id_by_len = sorted(
            identifiers, key=(lambda x: (len(x), x.lower())))

        similar = defaultdict(set)
        for id_list in (id_by_name, id_by_len):
            prev = None
            for cur in id_list:
                if prev:
                    lodiff = editdistance.eval(prev.lower(), cur.lower())
                    if (lodiff == 0 and (
                            (prev.isupper() and cur.islower()) or
                            (prev.islower() and cur.isupper()))):
                        pass
                    elif (prev.startswith('ARG') and
                            cur.startswith('ARG') and
                            prev[3:].isdigit() and
                            cur[3:].isdigit()):
                        # ARG1..n as passed to a Gosub() routine.
                        pass
                    elif (lodiff <= 2 and (lodiff + 1) < len(prev) and
                            (lodiff + 1) < len(cur)):
                        similar[prev].add(cur)
                        similar[cur].add(prev)
                prev = cur

        if similar:
            print('Identifiers with similar names include:')
            for identifier in sorted(
                    similar.keys(), key=(lambda x: x.lower())):
                similar_to = ', '.join(sorted(similar[identifier]))
                print('  {:32}  [similar to: {}]'.format(
                    identifier, similar_to))
            print()
            return 1


main = Main()
