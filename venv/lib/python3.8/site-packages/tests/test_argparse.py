import unittest

from myTree import mytree


class TestArgparse(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            # argv, [root directory, show_hidden, depth, simple]
            [['mytree'], [None, False, None, False]],
            [['mytree', '.'], ['.', False, None, False]],
            [['mytree', '-a'], [None, True, None, False]],
            [['mytree', 'foo/bar', '--show-hidden'], ['foo/bar', True, None, False]],
            [['mytree', '--depth', '1'], [None, False, 1, False]],
            [['mytree', 'bar/foo', '-d', '-1', '--show-hidden'], ['bar/foo', True, -1, False]],
            [['mytree', '--simple'], [None, False, None, True]],
            [['mytree', '-s', '--show-hidden'], [None, True, None, True]]
        ]

    def testArgparse(self):

        for argv, expected in self.test_cases:
            args = mytree.parse(argv=argv)
            self.assertEqual(args.root, expected[0])
            self.assertEqual(args.show_hidden, expected[1])
            self.assertEqual(args.depth, expected[2])
            self.assertEqual(args.simple, expected[3])
