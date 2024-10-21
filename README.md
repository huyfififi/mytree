The MyTree program is a customizable directory tree viewer that reads configurations from a `.mytree.json` file located in your home directory.

## Installation

```zsh
pip3 install --upgrade git+https://github.com/huyfififi/mytree.git@main
```

## Usage

```zsh
$ pwd
/Users/username/mytree

$ mytree
mytree (./)
├── LICENSE
├── pyproject.toml
├── README.md
└── mytree
    ├── decoration.py
    ├── __init__.py
    ├── tests.py
    └── main.py

$ mytree -a
mytree (./)
├── LICENSE
├── pyproject.toml
├── README.md
├── mytree
│   ├── decoration.py
│   ├── __init__.py
│   ├── tests.py
│   └── main.py
├── .gitignore
├── .github
│   └── workflows
│       ├── lint.yml
│       └── test.yml
├── .python-version
└── .mytree.json
```

## Configuration

### Supported Options

The `.mytree.json` configuration file currently supports the following options:

1. FILENAMES\_TO\_IGNORE

A list of file names to be excluded when displaying the directory tree. Files listed here will not be shown in the output.

1. DIRECTORY\_COLOR

Specifies the color to be used for displaying directory names. The value should be an integer representing a color in the range 0-255.

1. FILE_COLORS

A dictionary mapping file extensions to colors. Each file type will be displayed in the specified color. Colors should also be integers between 0 and 255.

### Character Color Ranges

Colors are represented using integers from 0 to 255, where each number corresponds to a specific color. To view the mapping of these numbers to their respective colors, you can run the following command:

```
python3 mytree/decoration.py
```

### Example

You can easily copy the configuration file from the repository to your home directory and begin customizing it.

Once you have created the .mytree.json file in your home directory with your desired settings, the program will automatically use the configuration whenever you run it.

```json
{
    "FILENAMES_TO_IGNORE": [".DS_Store", "Thumbs.db"],
    "DIRECTORY_COLOR": 34,
    "FILE_COLORS": {
        ".py": 82,
        ".md": 220,
        ".json": 100
    }
}
```
