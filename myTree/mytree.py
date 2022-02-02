import argparse
import os
import sys

import myTree
from myTree import display

from .constants import (
    COLOR_SUFFIXES,
    DIRECTORY_COLOR,
    IGNORE_FILES,
    SPACE,
)


def suffix(filename):
    return filename.split('.')[-1]


class TreeNode():

    def __init__(self, val=None, depth=0, dfc=None):
        self.val = val
        self.filename = self.val.split('/')[-1] if self.val else None
        self.children = []
        self.is_lastoflist = False
        self.parents_islast = []
        self.has_hidden = None
        self.depth = depth
        self.dfc = dfc

    def build_tree(self,
                   ignore_hidden=True, ignore_regular=False):
        listdir = os.listdir(self.val)
        listdir = [filename for filename in listdir if filename not in IGNORE_FILES]
        if ignore_hidden:
            listdir = [filename for filename in listdir if not filename.startswith(".")]
        listdir = [self.val + '/' + x for x in listdir]

        for i in range(len(listdir)):
            child = listdir[i]
            node = TreeNode(val=child, dfc=self.dfc, depth=self.depth + 1)
            if i == len(listdir) - 1:
                node.is_lastoflist = True
            node.parents_islast = self.parents_islast.copy()
            node.parents_islast.append(self.is_lastoflist)

            if os.path.isdir(node.val):
                node.build_tree(ignore_hidden=ignore_hidden,
                                ignore_regular=ignore_regular)

            self.children.append(node)

    def set_has_hidden_child(self):

        if len(self.children) == 0:
            if self.filename[0] == '.':
                self.has_hidden = True
            else:
                self.has_hidden = False
        else:
            self.has_hidden = False
            for child in self.children:
                child.set_has_hidden_child()
                self.has_hidden = self.has_hidden or child.has_hidden

    def print_tree(self, max_depth=None):
        if max_depth is not None and self.depth > max_depth:
            return

        list_lasts = self.parents_islast[1:]
        prefix = ''
        for is_last in list_lasts:
            if is_last:
                prefix = prefix + ' ' * (SPACE)
            else:
                prefix = prefix + '│' + ' ' * (SPACE - 1)
        if self.depth > 0:
            if self.is_lastoflist:
                prefix = prefix + '└' + '─' * (SPACE - 2) + ' '
            else:
                prefix = prefix + '├' + '─' * (SPACE - 2) + ' '
        print(prefix, end='')

        if os.path.isdir(self.val):
            self.dfc.set_char_with_n(DIRECTORY_COLOR)
            self.dfc.set_char_bold()
        if suffix_color_code := COLOR_SUFFIXES.get(suffix(self.filename)):
            self.dfc.set_char_with_n(suffix_color_code)
        if os.getcwd() == self.val:
            self.filename = self.filename + ' (./)'
        print(self.filename)
        if self.dfc.is_changed:
            self.dfc.reset_change()
        for child in self.children:
            child.print_tree(max_depth=max_depth)

    @staticmethod
    def print_tree_simple(filepath, depth, dfc, max_depth=None,
                          ignore_hidden=True):
        if max_depth is not None and depth > max_depth:
            return

        def _print_filename(filepath, depth, dfc=dfc):
            prefix = ' ' * 2 * depth + '|-'
            print(prefix, end='')

            filename = filepath.split('/')[-1]

            if os.path.isdir(filepath):
                dfc.set_char_with_n(DIRECTORY_COLOR)
                dfc.set_char_bold()
            if suffix_color_code := COLOR_SUFFIXES.get(suffix(filename)):
                dfc.set_char_with_n(suffix_color_code)

            print(filename)

            if dfc.is_changed:
                dfc.reset_change()

        _print_filename(filepath=filepath, depth=depth)

        listdir = os.listdir(filepath)
        listdir = [filename for filename in listdir if filename not in IGNORE_FILES]
        if ignore_hidden:
            listdir = [filename for filename in listdir if not filename.startswith(".")]
        listdir = [filepath + '/' + x for x in listdir]

        for childpath in listdir:
            if os.path.isdir(childpath):
                TreeNode.print_tree_simple(childpath, depth=depth + 1, dfc=dfc,
                                           ignore_hidden=ignore_hidden)
            else:
                _print_filename(filepath=childpath, depth=depth + 1)


def parse(argv=sys.argv):
    usage = 'mytree [ROOT_DIRECTORY] [-a --show-hidden] [-d --depth DEPTH] '\
            '[--only-hidden] [--find-hidden] [--simple] '\
            '[--ignore [LIST_OF_IGNORE_FILES]]'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument(
        'root',
        nargs='?',
        help='root directory')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=myTree.__version__,
        help='print product version and exit')
    parser.add_argument(
        '-a',
        '--show-hidden',
        action='store_true',
        help='also show hidden files')
    parser.add_argument(
        '-d',
        '--depth',
        type=int,
        help='set the maximum depth to show in graph')
    parser.add_argument(
        '-s',
        '--simple',
        action='store_true',
        help='show a simple tree')

    args = parser.parse_args(argv[1:])
    return args


def main():
    args = parse()
    if args.root is None:
        args.root = os.getcwd()
    else:
        # Absolute path
        if args.root[0] == '/':
            pass
        # Relative path
        else:
            args.root = os.getcwd() + '/' + args.root

    ignore_hidden = True
    if args.show_hidden:
        ignore_hidden = False

    if args.simple:
        TreeNode.print_tree_simple(args.root, depth=0,
                                   dfc=display.DisplayFormatChanger(),
                                   ignore_hidden=ignore_hidden)
        return

    root = TreeNode(val=args.root, dfc=display.DisplayFormatChanger())
    root.build_tree(ignore_hidden=ignore_hidden)

    root.print_tree(max_depth=args.depth)
