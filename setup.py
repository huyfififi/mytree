import setuptools
import distutils

import mytree

distutils.core.setup(
    name="mytree",
    version=mytree.__version__,
    description="simple tree implementation with python",
    url="https://github.com/huyfififi/mytree",
    packages=setuptools.find_packages(),
    python_requires=">=3.12",
    install_requires=[],
    entry_points={"console_scripts": ["mytree = mytree.mytree:main"]},
)
