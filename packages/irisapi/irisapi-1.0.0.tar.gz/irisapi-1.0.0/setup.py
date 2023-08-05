# Copyright (c) LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
# See LICENSE in the project root for license information.

import setuptools
import re

with open('src/iris/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

with open('README.md', 'r') as fd:
    long_description = fd.read()

setuptools.setup(
    name='irisapi',
    version=version,
    description='Iris is a highly configurable and flexible service for paging and messaging.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/linkedin/iris',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    include_package_data=True,
    install_requires=[
        'streql==3.0.2',
        'dnspython==1.16.0',
        'phonenumbers==7.4.1',
        'twilio==6.25.0',
        'google-api-python-client==1.4.2',
        'oauth2client==1.4.12',
        'slackclient==0.16',
        'PyYAML==3.13',
        'gevent==1.4.0',
        'falcon==1.1.0',
        'falcon-cors==1.1.2',
        'ujson==1.35',
        'requests==2.20.0',
        'PyMySQL==0.9.3',
        'SQLAlchemy==1.3.0',
        'Jinja2==2.10.1',
        'importlib==1.0.3',
        'Markdown==2.4.1',
        'click==6.6',
        'msgpack-python==0.4.5',
        'cssmin==0.2.0',
        'beaker==1.10.0',
        'cryptography==2.3',
        'webassets==0.12.1',
        'python-ldap==3.1.0',
        'exchangelib==2.1.0',
        'setproctitle==1.1.8',
        'pyfcm==1.4.3',
        'oncallclient==1.0.0',
        'idna==2.7',
        'pyqrcode==1.2.1'
    ],
    extras_require={
        'kazoo': ['kazoo==2.6.1'],
        # plugin deps
        'influxdb': ['influxdb'],
        'prometheus': ['prometheus_client'],
        'dev': [
            'gunicorn',
            'Sphinx==1.5.6',
            'sphinxcontrib-httpdomain',
            'sphinx_rtd_theme',
            # test deps
            'mock==2.0.0',
            'pytest==5.2.0',
            'pytest-mock==1.5.0',
            'pytest-cov',
            'flake8==3.5.0',
            'tox',
            'requests-mock==1.1.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'iris-dev = iris.bin.run_server:main',
            'iris = iris.bin.run_server:main',
            'iris-sender = iris.bin.sender:main',
            'iris-owa-sync = iris.bin.owasync:main',
            'iris-sync-targets = iris.bin.sync_targets:main',
            'iris-process-retention = iris.bin.retention:main',
            'iris-app-stats = iris.bin.app_stats:main',
            'iris_ctl = iris.bin.iris_ctl:main',
            'build_assets = iris.bin.ui_build_assets:main',
        ]
    }
)
