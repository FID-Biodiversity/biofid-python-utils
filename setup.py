from setuptools import setup, find_packages

setup(
    name='biofid-utils',
    version='0.1.1',
    author='Adrian Pachzelt',
    author_email='a.pachzelt@ub.uni-frankfurt.de',
    license='LICENSE.txt',
    description='Handy tools to apply to Django',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[
        "Django>=3.0",
        "webdriver-manager>=3.2.0",
        "selenium>=3.0.0"
    ],
)
