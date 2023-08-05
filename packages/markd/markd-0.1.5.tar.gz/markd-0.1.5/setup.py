"""
Project setup
"""
from os import path
import setuptools

# read the contents of your README file
CWD = path.abspath(path.dirname(__file__))
with open(path.join(CWD, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setuptools.setup(
    name="markd",
    version="0.1.5",
    author="Panagis Tselentis",
    author_email="tselentispanagis@gmail.com",
    description="",
    url="https://github.com/pantsel/markd",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=["markd", "markd.main"],
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries',
        'Environment :: Plugins',
    ],
)
