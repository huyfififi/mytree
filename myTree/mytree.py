import argparse
import os

from myTree import display


SPACE = 4


class TreeNode():

    def __init__(self, val=None):
        self.val = val
        self.children = []
        self.is_lastoflist = False
        self.parents_islast = []

    def buildTree(self, ignore_hidden=True):
        listdir = os.listdir(self.val)
        if ignore_hidden:
            listdir = [x for x in listdir if x[0] != '.']
        listdir = [self.val + '/' + x for x in listdir]

        for i in range(len(listdir)):
            child = listdir[i]
            node = TreeNode(val=child)
            if i == len(listdir)-1:
                node.is_lastoflist = True
            node.parents_islast = self.parents_islast.copy()
            node.parents_islast.append(self.is_lastoflist)

            if os.path.isdir(node.val):
                node.buildTree(ignore_hidden=ignore_hidden)

            self.children.append(node)

    def dfs(self):
        depth = len(self.parents_islast)
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
            es.setCharCyan()
        s = self.val.split('/')[-1]
        if os.getcwd() == self.val:
            s = s + ' (./)'
        print(s)
        if os.path.isdir(self.val):
            es.resetChar()
        for child in self.children:
            child.dfs()


def parse():
    usage = 'mytree [ROOT DIRECTORY]'
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument(
        'root',
        nargs='?',
        help='root directory')

    args = parser.parse_args()
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
    root = TreeNode(val=args.root)
    root.buildTree()
    root.dfs()
