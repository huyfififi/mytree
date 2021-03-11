import unittest

from myTree import mytree


class TestArgparse(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            [['mytree'], {'root_directory': None,
                          'show_hidden': False,
                          'only_hidden': False,
                          'find_hidden': False,
                          'depth': None,
                          'simple': False,
                          'ignore': None}],
            # check if args store bools
            [['mytree', '--show-hidden', '--only-hidden', '--find-hidden'],
             {'root_directory': None,
              'show_hidden': True,
              'only_hidden': True,
              'find_hidden': True,
              'depth': None,
              'simple': False,
              'ignore': None}],
            # test list args with one element
            [['mytree', '-s', '--depth', '3', '--ignore', '__pycache__'],
             {'root_directory': None,
              'show_hidden': False,
              'only_hidden': False,
              'find_hidden': False,
              'depth': 3,
              'simple': True,
              'ignore': ['__pycache__']}],
            # test list args with many elements
            [['mytree', 'ROOT_DIR', '--ignore', 'venv', 'tmp', 'tests'],
             {'root_directory': 'ROOT_DIR',
              'show_hidden': False,
              'only_hidden': False,
              'find_hidden': False,
              'depth': None,
              'simple': False,
              'ignore': ['venv', 'tmp', 'tests']}]
        ]

    def testArgparse(self):

        for argv, expected in self.test_cases:
            args = mytree.parse(argv)
            self.assertEqual(args.root, expected['root_directory'])
            self.assertEqual(args.show_hidden, expected['show_hidden'])
            self.assertEqual(args.only_hidden, expected['only_hidden'])
            self.assertEqual(args.find_hidden, expected['find_hidden'])
            self.assertEqual(args.depth, expected['depth'])
            self.assertEqual(args.simple, expected['simple'])
            self.assertEqual(args.ignore, expected['ignore'])
