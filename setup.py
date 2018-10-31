from distutils.core import setup
from setuptools import find_packages, Extension

setup(
    name='liang',
    version='0.4',
    url='',
    license='',
    author='LiangGongxun',
    description='this is a test for setup tool',
    long_description="this package include a pack which is named by liang. "
                     "the package has no use just a test",
    entry_points={
        'console_scripts': [
            'liangtest = liang.manger:main',
        ],
    },
    packages=["liang"], install_requires=['pymongo']
)
