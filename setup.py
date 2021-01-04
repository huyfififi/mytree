import setuptools
import distutils

distutils.core.setup(
    name='myTree',
    version='0.0.1',
    description='Display Directory Tree',
    author='Kazuki Nguyen',
    url='https://github.com/hn_void/myTree',
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'mytree = myTree.mytree:main'
        ]
    }
)
