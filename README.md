## myTree

### Install & Upgrade

```
$ pip3 install --upgrade git+https://github.com/huyvnguyen/myTree.git@main
```

### Configure Colors by Yourself
```
$ git clone https://github.com/huyvnguyen/myTree.git
$ cd myTree
$ cat myTree/__init__.py
__version__ = '0.1.1'

# 1~256
# You can check the colors by 'python3 display.py'
directory_color = 4
color_suffixes = [('py', 14)]

$ pip3 install --upgrade .
$ mytree tests/test_files
```
![configure_color.png](/docs/configure_color.png)


### Usage example

```
$ pwd
/home/YOUR_NAME/myTree/tests/test_files


$ mytree --help
usage: mytree [ROOT_DIRECTORY] [-a --show-hidden] [-d --depth DEPTH] [--only-hidden] [--find-hidden] [--simple] [--ignore [LIST_OF_IGNORE_FILES]]

positional arguments:
  root                  root directory

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print product version and exit
  -a, --show-hidden     also show hidden files
  --only-hidden         show only hidden paths
  --find-hidden         find hidden files
  -d DEPTH, --depth DEPTH
                        set the maximum depth to show in graph
  -s, --simple          show a simple tree
  --ignore [IGNORE [IGNORE ...]]
                        set specific ignore files


$ mytree
test_files (./)
├── a_1.txt
├── a_2.py
└── A_1
    ├── B_2
    │   ├── C_1
    │   └── c_2.docx
    ├── b_1.ml
    └── b_2.hs


$ mytree -a
test_files (./)
├── a_1.txt
├── a_2.py
├── .a_3.c
├── .A_2
│   ├── b_4.cpp
│   └── B_3
│       └── c_1.docx
└── A_1
    ├── B_2
    │   ├── C_1
    │   │   └── .d_4.jpeg
    │   └── c_2.docx
    ├── .B_1
    │   ├── C_1
    │   │   ├── d_1.md
    │   │   └── d_2.md
    │   └── C_2
    │       └── d_3.md
    ├── b_1.ml
    ├── .b_3.lisp
    └── b_2.hs


$ mytree A_1/B_2
B_2
├── C_1
└── c_2.docx


$ mytree -d 2
test_files (./)
├── a_1.txt
├── a_2.py
└── A_1
    ├── B_2
    ├── b_1.ml
    └── b_2.hs


$ mytree --only-hidden
test_files (./)
├── .a_3.c
└── .A_2


$ mytree --find-hidden
test_files (./)
├── .a_3.c
└── A_1
    ├── B_2
    │   └── C_1
    │       └── .d_4.jpeg
    └── .b_3.lisp


$ mytree --simple
|-test_files
  |-a_1.txt
  |-a_2.py
  |-A_1
    |-B_2
      |-C_1
      |-C_1
      |-c_2.docx
    |-B_2
    |-b_1.ml
    |-b_2.hs
  |-A_1


$ mytree --ignore B_2 a_2.py
test_files (./)
├── a_1.txt
└── A_1
    ├── b_1.ml
    └── b_2.hs


```
