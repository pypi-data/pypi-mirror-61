# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
setup(
    name="gen_name_szczep",
    version= "0.1.1",
    author="Szczepanek LTD",
    author_email= "szczepanek.pdm@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    description="Super useful library",
    url="http://github.com/treyhunner/names",
    scripts=["gen_names_szczep/gen_name_szczep.py", "bin/gen_name_szczep.sh"],
    install_requires=["names"]
)

