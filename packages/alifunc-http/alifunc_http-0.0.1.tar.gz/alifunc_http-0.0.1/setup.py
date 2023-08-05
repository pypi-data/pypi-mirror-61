try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from setuptools import find_packages


setup(
    name='alifunc_http',
    author='cbnSpider',
    version='0.0.1',
    description='Ali serverless http client',
    url='https://github.com/TapasTech/alifunc_invoke',
    packages=find_packages(),
    install_requires=[
        'requests >= 2.22.0',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
)