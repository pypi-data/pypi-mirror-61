from setuptools import setup, find_packages

setup(
    name='gen_names_mkopys',
    version='1.0.0',
    description="Generate random names with lenght mkopys",
    long_description='Generate random names with lenght mkopys',
    url="https://github.com/treyhunner/names",
    author='Michal Kopys',
    author_email='mikopys@gmail.com',
    include_package_data=True,
    keywords='random names',
    packages=find_packages(),
    scripts=['gen_names_mkopys/gen_names_mkopys.py', 'bin/gen_names_mkopys.bat'],
    install_requires=['names']
)
