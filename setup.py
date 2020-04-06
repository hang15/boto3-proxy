from setuptools import setup

setup(
    name='boto3proxy',
    version='0.0.1',
    description='Proxy for Boto3',
    license='unlicense',
    packages=['boto3proxy'],
    zip_safe=False,
    install_requires=[
        'starlette',
        'boto3'
    ],
)
