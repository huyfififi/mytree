## myTree

### Installation

```
$ pip install git+https://github.com/hn-void/myTree.git@main
```

### Usage example

```
$ pwd
/Users/YOUR_NAME/myTree/tests/test_file

$ mytree
test_file (./)
├── a
│   ├── b2.txt
│   ├── b1.txt
│   └── c
│       ├── c1.txt
│       └── d
│           ├── d1.txt
│           ├── d2.txt
│           └── d3.txt
└── a.txt

$ mytree -a
test_file (./)
├── a
│   ├── b2.txt
│   ├── b1.txt
│   ├── .b
│   │   ├── e2
│   │   │   ├── f4
│   │   │   └── f3
│   │   ├── e.txt
│   │   └── e1
│   │       ├── f2
│   │       └── f1
│   └── c
│       ├── c1.txt
│       ├── .c2.txt
│       └── d
│           ├── d1.txt
│           ├── d2.txt
│           └── d3.txt
└── a.txt

$ mytree a/c
c
├── c1.txt
└── d
    ├── d1.txt
    ├── d2.txt
    └── d3.txt

$ mytree /Users/ci11y/myTree/tests/test_file/a/.b
.b
├── e2
│   ├── f4
│   └── f3
├── e.txt
└── e1
    ├── f2
    └── f1
```
