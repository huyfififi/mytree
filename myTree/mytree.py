import os

from myTree import display


SPACE = 4


class TreeNode():

    def __init__(self, val=None):
        self.val = val
        self.parent = None
        self.children = []
        self.child_num = 0
        self.depth = 0
        self.is_lastoflist = False
        self.last_count = 0

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
            node.depth = self.depth + 1
            node.parent = self
            if self.is_lastoflist:
                node.last_count = self.last_count + 1
            else:
                node.last_count = self.last_count
            if os.path.isdir(node.val):
                node.buildTree(ignore_hidden=ignore_hidden)
            self.children.append(node)

    def dfs(self):
        prefix = ''
        prefix = '│' + ' '*(SPACE-1)
        prefix = prefix * (self.depth-1-self.last_count)
        if self.depth > 0:
            if self.depth > 1:
                prefix = prefix + (' '*(SPACE))*self.last_count
            if self.is_lastoflist:
                prefix = prefix + '└' + '─'*(SPACE-2) + ' '
            else:
                prefix = prefix + '├' + '─'*(SPACE-2) + ' '
        print(prefix, end='')
        es = display.EscapeSequence()
        if os.path.isdir(self.val):
            es.setCharCyan()
        print(self.val.split('/')[-1], self.last_count, self.is_lastoflist)
        if os.path.isdir(self.val):
            es.resetChar()
        for child in self.children:
            child.dfs()

    def countAllChildren(self):
        pass


def main():
    root = TreeNode(val=os.getcwd())
    root.buildTree()
    root.dfs()
