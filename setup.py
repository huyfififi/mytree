import setuptools
import distutils

import myTree

distutils.core.setup(
    name='myTree',
    version=myTree.__version__,
    description='Display Directory Tree',
    author='Kazuki Nguyen',
    url='https://github.com/hn-void/myTree',
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'mytree = myTree.mytree:main'
        ]
    }
)
