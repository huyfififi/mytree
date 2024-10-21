import argparse
import json
import os
import sys

import mytree
from mytree import decoration
from mytree.decoration import pretty_print

from mytree.constants import (
    COLOR_SUFFIXES,
    DIRECTORY_COLOR,
    SPACE,
)


class MyTreeConfig:
    KEY_FILENAMES_TO_IGNORE = "FILENAMES_TO_IGNORE"
    KEY_DIRECTORY_COLOR = "DIRECTORY_COLOR"
    DEFAULT_DIRECTORY_COLOR = 202

    def __update_config(self, config: dict) -> None:
        if self.KEY_FILENAMES_TO_IGNORE in config:
            self.filenames_to_ignore = config[self.KEY_FILENAMES_TO_IGNORE]
            assert isinstance(self.filenames_to_ignore, list) and all(
                isinstance(x, str) for x in self.filenames_to_ignore
            ), "FILENAMES_TO_IGNORE must be a list of strings"

        if self.KEY_DIRECTORY_COLOR in config:
            self.directory_color = config[self.KEY_DIRECTORY_COLOR]
            assert isinstance(
                self.directory_color, int
            ), "DIRECTORY_COLOR must be an integer"
            assert 0 <= self.directory_color <= 255, "DIRECTORY_COLOR must be 0~255"

    def __init__(self, filename: str = ".mytree.json") -> None:
        self.filenames_to_ignore = []
        self.directory_color = self.DEFAULT_DIRECTORY_COLOR

        # Update config from file if exists
        config_path: str = os.path.expanduser(f"~/{filename}")
        if not os.path.exists(config_path):
            return

        with open(config_path, "r") as f:
            self.__update_config(json.loads(f.read()))

        return


def suffix(filename):
    return filename.split(".")[-1]


class TreeNode:
    def __init__(self, config: MyTreeConfig, val=None, depth=0, dfc=None):
        self.val = val
        self.filename = self.val.split("/")[-1] if self.val else None
        self.children = []
        self.is_lastoflist = False
        self.parents_islast = []
        self.has_hidden = None
        self.depth = depth
        self.dfc = dfc
        self.config = config

    def build_tree(
        self,
        ignore_hidden=True,
        ignore_regular=False,
    ):
        listdir = os.listdir(self.val)
        listdir = [
            filename
            for filename in listdir
            if filename not in (self.config.filenames_to_ignore or [])
        ]
        if ignore_hidden:
            listdir = [filename for filename in listdir if not filename.startswith(".")]
        listdir = [self.val + "/" + x for x in listdir]

        for i in range(len(listdir)):
            child = listdir[i]
            node = TreeNode(
                val=child, dfc=self.dfc, depth=self.depth + 1, config=self.config
            )
            if i == len(listdir) - 1:
                node.is_lastoflist = True
            node.parents_islast = self.parents_islast.copy()
            node.parents_islast.append(self.is_lastoflist)

            if os.path.isdir(node.val):
                node.build_tree(
                    ignore_hidden=ignore_hidden, ignore_regular=ignore_regular
                )

            self.children.append(node)

    def set_has_hidden_child(self):
        if len(self.children) == 0:
            if self.filename[0] == ".":
                self.has_hidden = True
            else:
                self.has_hidden = False
        else:
            self.has_hidden = False
            for child in self.children:
                child.set_has_hidden_child()
                self.has_hidden = self.has_hidden or child.has_hidden

    def print_tree(self):
        list_lasts = self.parents_islast[1:]
        prefix = ""
        for is_last in list_lasts:
            if is_last:
                prefix = prefix + " " * (SPACE)
            else:
                prefix = prefix + "│" + " " * (SPACE - 1)
        if self.depth > 0:
            if self.is_lastoflist:
                prefix = prefix + "└" + "─" * (SPACE - 2) + " "
            else:
                prefix = prefix + "├" + "─" * (SPACE - 2) + " "
        print(prefix, end="")

        if os.path.isdir(self.val):
            self.dfc.set_char_with_n(DIRECTORY_COLOR)
            self.dfc.set_char_bold()
        if suffix_color_code := COLOR_SUFFIXES.get(suffix(self.filename)):
            self.dfc.set_char_with_n(suffix_color_code)
        if os.getcwd() == self.val:
            self.filename = self.filename + " (./)"
        print(self.filename)
        if self.dfc.is_changed:
            self.dfc.reset_change()
        for child in self.children:
            child.print_tree()

    @staticmethod
    def print_tree_simple(
        filepath,
        depth,
        config: MyTreeConfig,
        ignore_hidden=True,
    ):
        def _print_filename(filepath, depth):
            prefix = " " * 2 * depth + "|-"
            print(prefix, end="")

            filename = filepath.split("/")[-1]

            if os.path.isdir(filepath):
                pretty_print(filename, color=config.directory_color, bold=True)
            elif suffix_color_code := COLOR_SUFFIXES.get(suffix(filename)):
                pretty_print(filename, color=suffix_color_code)
            else:
                print(filename)

        _print_filename(filepath=filepath, depth=depth)

        listdir = os.listdir(filepath)
        listdir = [
            filename
            for filename in listdir
            if filename not in (config.filenames_to_ignore or [])
        ]
        if ignore_hidden:
            listdir = [filename for filename in listdir if not filename.startswith(".")]
        listdir = [filepath + "/" + x for x in listdir]

        for childpath in listdir:
            if os.path.isdir(childpath):
                TreeNode.print_tree_simple(
                    childpath,
                    depth=depth + 1,
                    ignore_hidden=ignore_hidden,
                    config=config,
                )
            else:
                _print_filename(filepath=childpath, depth=depth + 1)


def parse(argv=sys.argv):
    usage = "mytree [ROOT_DIRECTORY] [-a --show-hidden] " "[--simple]"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("root", nargs="?", help="root directory")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=mytree.__version__,
        help="print product version and exit",
    )
    parser.add_argument(
        "-a", "--show-hidden", action="store_true", help="also show hidden files"
    )
    parser.add_argument(
        "-s", "--simple", action="store_true", help="show a simple tree"
    )

    args = parser.parse_args(argv[1:])
    return args


def main():
    args = parse()
    if args.root is None:
        args.root = os.getcwd()
    else:
        # Absolute path
        if args.root[0] == "/":
            pass
        # Relative path
        else:
            args.root = os.getcwd() + "/" + args.root

    ignore_hidden = True
    if args.show_hidden:
        ignore_hidden = False

    config = MyTreeConfig()

    if args.simple:
        TreeNode.print_tree_simple(
            args.root,
            depth=0,
            ignore_hidden=ignore_hidden,
            config=config,
        )
        return

    root = TreeNode(
        val=args.root,
        dfc=decoration.DisplayFormatChanger(),
        config=config,
    )
    root.build_tree(ignore_hidden=ignore_hidden)

    root.print_tree()
