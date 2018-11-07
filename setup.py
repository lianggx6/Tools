# -*- coding: utf-8 -*-
# @Time    : 2018/7/25 15:10
# @Author  : tao.shao
# @File    : setup.py

from distutils.core import setup
# from Cython.Build import cythonize

setup(
    # ext_modules=cythonize("parser.pyx"),
    name='kgi_parser',
    version=0.1,
    description="Parse the KGI data in the computer",
    author="LiangGongxun",
    author_email="lianggx@jyquant.com.cn",
    packages=["kgi_parser"]
)
