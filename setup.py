import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pypong",
    version = "0.0.1",
    author = "Brian Guan",
    author_email = "brian.guan@gmail.com",
    description = ("Classic Pong using simple Pygame for demo purpose."),
    license = "Apache",
    keywords = "pong pygame demo",
    url = "http://github.com/bguan/pypong",
    packages=['pypong', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Game",
        "License :: OSI Approved :: Apache License",
    ],
    install_requires=[
       'pygame>=2.0.0.dev12'
    ]
)
