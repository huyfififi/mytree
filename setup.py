import setuptools
import distutils

import mytree

distutils.core.setup(
    name="mytree",
    version=mytree.__version__,
    description="Display Directory Tree",
    url="https://github.com/hn-void/mytree",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    entry_points={"console_scripts": ["mytree = mytree.mytree:main"]},
)
