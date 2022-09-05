from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='idoitapi',
    version='1.0b2',

    description='i-doit JSON RPC API',
    long_description="Python implementation of Benjamin Heisig's PHP-based i-doit API client library",
    license='AGPLv3+',
    # url='',
    platforms=['any'],

    zip_safe=False,
    author='Martin Vorländer',
    author_email='mv@pdv-systeme.de',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='i-doit',

    python_requires='>=3.0',
    # scripts=[''],
    packages=[
        'idoitapi'
    ],
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    extras_require={
        'docs': ['Sphinx'],
    },
    test_suite='nose.collector',
    tests_require=[
        'nose'
    ],
)
