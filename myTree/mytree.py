import os

from myTree import display


class TreeNode():

    def __init__(self, val=None):
        self.val = val
        self.children = []
        self.child_num = 0
        self.depth = 0

    def buildTree(self, ignore_hidden=True):
        listdir = os.listdir(self.val)
        if ignore_hidden:
            listdir = [x for x in listdir if x[0] != '.']
        listdir = [self.val + '/' + x for x in listdir]

        for child in listdir:
            node = TreeNode(val=child)
            node.depth = self.depth + 1
            if os.path.isdir(node.val):
                node.buildTree(ignore_hidden=ignore_hidden)
            self.children.append(node)

    def dfs(self):
        es = display.EscapeSequence()
        if os.path.isdir(self.val):
            es.setCharCyan()
        print('    '*self.depth, self.val.split('/')[-1], sep='')
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
