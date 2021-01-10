import sys
import unittest

from myTree import mytree


# Need improvement
# How about Dependency Injection?
class TestArgparse(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            # argv: [root directory, show_hidden]
            [['mytree'], [None, False, None]],
            [['mytree', '.'], ['.', False, None]],
            [['mytree', '-a'], [None, True, None]],
            [['mytree', 'foo/bar', '--show-hidden'], ['foo/bar', True, None]],
            [['mytree', '--depth', '1'], [None, False, 1]],
            [['mytree', 'bar/foo', '-d', '-1', '--show-hidden'], ['bar/foo', True, -1]]
        ]

    def testArgparse(self):

        for argv, expected in self.test_cases:
            sys.argv = argv
            args = mytree.parse()
            self.assertEqual(args.root, expected[0])
            self.assertEqual(args.show_hidden, expected[1])
            self.assertEqual(args.depth, expected[2])
