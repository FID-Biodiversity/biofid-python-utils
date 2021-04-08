from setuptools import setup

setup(
    name='biofid-utils',
    version='0.1.0',
    author='Adrian Pachzelt',
    author_email='a.pachzelt@ub.uni-frankfurt.de',
    license='LICENSE.txt',
    description='Handy tools to apply to Django',
    long_description=open('README.md').read(),
    install_requires=[
        "Django==3.0",
        "webdriver-manager==3.3.0",
        "selenium==3.141.0"
    ],
)