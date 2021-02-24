import argparse
import os
import sys

import myTree
from myTree import display, directory_color, color_suffixes


SPACE = 4


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

    @staticmethod
    def filter_files(listdir, ignore_hidden=True,
                     ignore_regular=False, ignore_files=None):
        if ignore_hidden:
            listdir = [x for x in listdir if x[0] != '.']
        if ignore_regular:
            listdir = [x for x in listdir if x[0] == '.']
        if ignore_files is not None:
            listdir = [x for x in listdir if x not in ignore_files]
        return listdir

    def build_tree(self,
                   ignore_hidden=True, ignore_regular=False,
                   ignore_files=None):
        listdir = os.listdir(self.val)
        listdir = TreeNode.filter_files(listdir,
                                        ignore_hidden=ignore_hidden,
                                        ignore_regular=ignore_regular,
                                        ignore_files=ignore_files)
        listdir = [self.val + '/' + x for x in listdir]

        for i in range(len(listdir)):
            child = listdir[i]
            node = TreeNode(val=child, dfc=self.dfc, depth=self.depth+1)
            if i == len(listdir)-1:
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

    def prune_regular_file(self):
        new_children = []
        for child in self.children:
            child.prune_regular_file()
            if child.has_hidden:
                new_children.append(child)
        self.children = new_children

    def set_last_again(self):
        if len(self.children) > 0:
            for i in range(len(self.children)):
                self.children[i].is_lastoflist = False
                if i == len(self.children)-1:
                    self.children[i].is_lastoflist = True
                self.children[i].parents_islast = self.parents_islast.copy()
                self.children[i].parents_islast.append(self.is_lastoflist)
                self.children[i].set_last_again()

    def print_tree(self, max_depth=None):
        if max_depth is not None and self.depth > max_depth:
            return

        list_lasts = self.parents_islast[1:]
        prefix = ''
        for is_last in list_lasts:
            if is_last:
                prefix = prefix + ' '*(SPACE)
            else:
                prefix = prefix + '│' + ' '*(SPACE-1)
        if self.depth > 0:
            if self.is_lastoflist:
                prefix = prefix + '└' + '─'*(SPACE-2) + ' '
            else:
                prefix = prefix + '├' + '─'*(SPACE-2) + ' '
        print(prefix, end='')

        if os.path.isdir(self.val):
            self.dfc.set_char_with_n(directory_color)
            self.dfc.set_char_bold()
        for color_suffix in color_suffixes:
            if suffix(self.filename) == color_suffix[0]:
                self.dfc.set_char_with_n(color_suffix[1])
                break
        if os.getcwd() == self.val:
            self.filename = self.filename + ' (./)'
        print(self.filename)
        if self.dfc.is_changed:
            self.dfc.reset_change()
        for child in self.children:
            child.print_tree(max_depth=max_depth)

    @staticmethod
    def print_tree_simple(filepath, depth, dfc, max_depth=None,
                          ignore_hidden=True, ignore_regular=False,
                          ignore_files=None):
        if max_depth is not None and depth > max_depth:
            return

        def _print_filename(filepath, depth, dfc=dfc):
            prefix = ' ' * 2 * depth + '|-'
            print(prefix, end='')

            filename = filepath.split('/')[-1]

            if os.path.isdir(filepath):
                dfc.set_char_with_n(directory_color)
                dfc.set_char_bold()
            for color_suffix in color_suffixes:
                if suffix(filename) == color_suffix[0]:
                    dfc.set_char_with_n(color_suffix[1])

            print(filename)

            if dfc.is_changed:
                dfc.reset_change()

        _print_filename(filepath=filepath, depth=depth)

        listdir = os.listdir(filepath)
        listdir = TreeNode.filter_files(listdir,
                                        ignore_hidden=ignore_hidden,
                                        ignore_regular=ignore_regular,
                                        ignore_files=ignore_files)
        listdir = [filepath + '/' + x for x in listdir]

        for childpath in listdir:
            if os.path.isdir(childpath):
                TreeNode.print_tree_simple(childpath, depth+1, dfc=dfc,
                                           ignore_hidden=ignore_hidden,
                                           ignore_regular=ignore_regular)
            _print_filename(filepath=childpath, depth=depth+1)


def parse(argv=sys.argv):
    usage = 'mytree [ROOT_DIRECTORY] [-a --show-hidden] [-d --depth DEPTH]\
    [--only-hidden] [--find-hidden] [--simple]\
    [--ignore [LIST_OF_IGNORE_FILES]]'
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
        '--only-hidden',
        action='store_true',
        help='show only hidden paths')
    parser.add_argument(
        '--find-hidden',
        action='store_true',
        help='find hidden files')
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
    parser.add_argument(
        '--ignore',
        nargs='*',
        help='set specific ignore files')

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
    ignore_regular = False
    if args.show_hidden:
        ignore_hidden = False
    if args.only_hidden:
        ignore_hidden = False
        ignore_regular = True
    if args.find_hidden:
        ignore_hidden = False

    if args.simple:
        TreeNode.print_tree_simple(args.root, depth=0,
                                   dfc=display.DisplayFormatChanger(),
                                   ignore_hidden=ignore_hidden,
                                   ignore_regular=ignore_regular,
                                   ignore_files=args.ignore)
        return

    root = TreeNode(val=args.root, dfc=display.DisplayFormatChanger())
    root.build_tree(ignore_hidden=ignore_hidden,
                    ignore_regular=ignore_regular,
                    ignore_files=args.ignore)
    # The process for --find-hidden seems not efficient
    if args.find_hidden:
        root.set_has_hidden_child()
        root.prune_regular_file()
        root.set_last_again()

    root.print_tree(max_depth=args.depth)
