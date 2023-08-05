from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='onnpdf',
    version='0.0.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='http://oznetnerd.com',
    install_requires=[
        'WeasyPrint >= 51',
        'Jinja2 >= 2.11.1',
    ],
    license='',
    author='Will Robinson',
    author_email='will@oznetnerd.com',
    description='Convenience Python module for creating templated PDF documents'
)
