import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='AkvoResponseGrouper',
    author='Akvo',
    author_email='tech.consultancy@akvo.org',
    description='Fast-API Response catalog for pre-computed query',
    keywords='akvo, data, helper, pypi, package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/akvo/Akvo-ResponseGrouper',
    project_urls={
        'Documentation': 'https://github.com/akvo/Akvo-ResponseGrouper',
        'Bug Reports':
        'https://github.com/akvo/Akvo-ResponseGrouper/issues',
        'Source Code': 'https://github.com/akvo/Akvo-ResponseGrouper',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Database :: Database Engines/Servers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Framework :: FastAPI',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8.5',
    install_requires=['pandas', 'pydantic'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # for generate db etc
    #         'migrate=migrate:main',
    #          to run `main()` in src/migrate/__init__.py
    #         'destroy=destroy:main',
    #          to run `main()` in src/rollback/__init__.py
    #         'generate_config=generate_config:main',
    #          to run `main()` in src/generate_config/__init__.py
    #     ],
    # },
)
