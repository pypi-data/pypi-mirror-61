from setuptools import setup, find_packages

setup(
    name='easyqueue-core',
    version='0.0.0',
    description='Easy queue basic model',
    url='https://github.com/Bignone/easy-queue-core.git',
    author='Eduardo Bustos',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='rest restful api swagger openapi eq-object',

    packages=find_packages(),

    install_requires=[
        'schema'
        ],
)
