from setuptools import find_packages, setup

setup(
    name='my_names_lib_x',
    version='1.0',
    author='mmm',
    description='Generate random names with length',
    author_email='mmm@Company.com',
    packages=find_packages(),
    include_packages_data=True,
    url='https://github.com',
    keywords='random.names',
    scripts=['my_names/get_names.py', 'my_names/bin/get_names.bat'],
    install_requiers=['names']

)
