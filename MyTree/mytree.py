import os

import display


class TreeNode():

    def __init__(self, val=None):
        self.val = val
        self.children = []
        self.child_num = 0
        self.depth = 0

    def buildTree(self, ignore_hidden=True):
        print('PARENT:', self.val)
        listdir = os.listdir(self.val)
        if ignore_hidden:
            listdir = [x for x in listdir if x[0] != '.']
        listdir = [self.val + '/' + x for x in listdir]
        print(listdir)

        for child in listdir:
            print(child)
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


if __name__ == '__main__':
    root = TreeNode(val=os.getcwd())
    root.buildTree()
    print('-'*80)
    print(root.children)
    for child in root.children:
        print(child.val)
    root.dfs()
