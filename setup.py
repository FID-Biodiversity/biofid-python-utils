from setuptools import setup, find_packages

setup(
    name='biofid-python-utils',
    version='0.2.2',
    author='Adrian Pachzelt',
    author_email='a.pachzelt@ub.uni-frankfurt.de',
    license='',
    description='Handy tools to apply to Django',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[
        "Django>=3.0",
    ],
    extras_require={
        'dev': [
            "webdriver-manager>=3.2.0",
            "selenium>=3.0.0",
            'pytest-django'
        ]
    }
)
