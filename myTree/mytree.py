import argparse
import os
import sys

import myTree
from myTree import display


SPACE = 4


class TreeNode():

    def __init__(self, val=None, es=None):
        self.val = val
        self.children = []
        self.is_lastoflist = False
        self.parents_islast = []
        self.es = es

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
            node.es = self.es

            if os.path.isdir(node.val):
                node.buildTree(ignore_hidden=ignore_hidden, ignore_regular=ignore_regular)

            self.children.append(node)

    def dfs(self, max_depth=None):
        depth = len(self.parents_islast)
        if max_depth is not None and depth > max_depth:
            return
        list_lasts = self.parents_islast[1:]
        prefix = ''
        for is_last in list_lasts:
            if is_last:
                prefix = prefix + ' '*(SPACE)
            else:
                prefix = prefix + '│' + ' '*(SPACE-1)
        if depth > 0:
            if self.is_lastoflist:
                prefix = prefix + '└' + '─'*(SPACE-2) + ' '
            else:
                prefix = prefix + '├' + '─'*(SPACE-2) + ' '
        print(prefix, end='')
        es = display.EscapeSequence()
        if os.path.isdir(self.val):
            self.es.setCharN(211)
            self.es.setCharBold()
        s = self.val.split('/')[-1]
        if os.getcwd() == self.val:
            s = s + ' (./)'
        print(s)
        if os.path.isdir(self.val):
            es.resetChar()
        for child in self.children:
            child.dfs(max_depth=max_depth)


def parse(argv=sys.argv):
    usage = 'mytree [ROOT DIRECTORY] [-a --show-hidden] [-d --depth]'
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
        help='show only hidden files')
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

    root.buildTree(ignore_hidden=ignore_hidden, ignore_regular=ignore_regular)
    root.dfs(max_depth=args.depth)
