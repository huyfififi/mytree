import argparse
import os
import sys

import myTree
from myTree import display, directory_color, color_suffixes


SPACE = 4


def suffix(filename):
    return filename.split('.')[-1]


class TreeNode():

    def __init__(self, val=None, es=None):
        self.val = val
        self.filename = self.val.split('/')[-1] if self.val else None
        self.children = []
        self.is_lastoflist = False
        self.parents_islast = []
        self.es = es
        self.has_hidden = None
        self.depth = 0

    def buildTree(self, ignore_hidden=True, ignore_regular=False):
        listdir = os.listdir(self.val)
        if ignore_hidden:
            listdir = [x for x in listdir if x[0] != '.']
        if ignore_regular:
            listdir = [x for x in listdir if x[0] == '.']
        listdir = [self.val + '/' + x for x in listdir]

        for i in range(len(listdir)):
            child = listdir[i]
            node = TreeNode(val=child)
            if i == len(listdir)-1:
                node.is_lastoflist = True
            node.parents_islast = self.parents_islast.copy()
            node.parents_islast.append(self.is_lastoflist)
            node.depth = self.depth+1
            node.es = self.es

            if os.path.isdir(node.val):
                node.buildTree(ignore_hidden=ignore_hidden, ignore_regular=ignore_regular)

            self.children.append(node)

    def buildTreeSimple(self, ignore_hidden=True, ignore_regular=False):
        listdir = os.listdir(self.val)
        if ignore_hidden:
            listdir = [x for x in listdir if x[0] != '.']
        if ignore_regular:
            listdir = [x for x in listdir if x[0] == '.']
        listdir = [self.val + '/' + x for x in listdir]

        for child in listdir:
            node = TreeNode(val=child)
            node.depth = self.depth+1
            node.es = self.es
            if os.path.isdir(node.val):
                node.buildTreeSimple(ignore_hidden=ignore_hidden, ignore_regular=ignore_regular)
            self.children.append(node)

    def setHasHiddenChild(self):

        if len(self.children) == 0:
            if self.filename[0] == '.':
                self.has_hidden = True
            else:
                self.has_hidden = False
        else:
            self.has_hidden = False
            for child in self.children:
                child.setHasHiddenChild()
                self.has_hidden = self.has_hidden or child.has_hidden

    def pruneRegularFile(self):
        new_children = []
        for child in self.children:
            child.pruneRegularFile()
            if child.has_hidden:
                new_children.append(child)
        self.children = new_children

    def setLastAgain(self):
        if len(self.children) > 0:
            for i in range(len(self.children)):
                self.children[i].is_lastoflist = False
                if i == len(self.children)-1:
                    self.children[i].is_lastoflist = True
                self.children[i].parents_islast = self.parents_islast.copy()
                self.children[i].parents_islast.append(self.is_lastoflist)
                self.children[i].setLastAgain()

    def printTree(self, max_depth=None):
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
        es = display.EscapeSequence()
        change_flag = False
        if os.path.isdir(self.val):
            self.es.setCharN(directory_color)
            self.es.setCharBold()
            change_flag = True
        for color_suffix in color_suffixes:
            if suffix(self.filename) == color_suffix[0]:
                self.es.setCharN(color_suffix[1])
                change_flag = True
                break
        if os.getcwd() == self.val:
            self.filename = self.filename + ' (./)'
        print(self.filename)
        if change_flag:
            es.resetChange()
        for child in self.children:
            child.printTree(max_depth=max_depth)

    def printTreeSimple(self, max_depth=None):
        if max_depth is not None and self.depth > max_depth:
            return
        prefix = self.depth * 2 * ' ' + '|-'
        print(prefix, end='')
        change_flag = False
        if os.path.isdir(self.val):
            self.es.setCharN(directory_color)
            self.es.setCharBold()
            change_flag = True
        for color_suffix in color_suffixes:
            if suffix(self.filename) == color_suffix[0]:
                self.es.setCharN(color_suffix[1])
                change_flag = True
                break
        if os.getcwd() == self.val:
            self.filename = self.filename + ' (./)'
        print(self.filename)
        if change_flag:
            self.es.resetChange()
        for child in self.children:
            child.printTreeSimple(max_depth=max_depth)


def parse(argv=sys.argv):
    usage = 'mytree [ROOT_DIRECTORY] [-a --show-hidden] [-d --depth DEPTH] [--only-hidden] [--find-hidden] [--simple]'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument(
        'root',
        nargs='?',
        help='root directory')
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
        '-v',
        '--version',
        action='version',
        version=myTree.__version__,
        help='print product version and exit')
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
    root = TreeNode(val=args.root, es=display.EscapeSequence())

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
        root.buildTreeSimple(ignore_hidden=ignore_hidden, ignore_regular=ignore_regular)
    else:
        root.buildTree(ignore_hidden=ignore_hidden, ignore_regular=ignore_regular)
    # The process for --find-hidden seems not efficient
    if args.find_hidden:
        root.setHasHiddenChild()
        root.pruneRegularFile()
        root.setLastAgain()
    if args.simple:
        root.printTreeSimple(max_depth=args.depth)
    else:
        root.printTree(max_depth=args.depth)
