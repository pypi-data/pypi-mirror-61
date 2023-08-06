# -{del dist\* | python %f sdist bdist_wheel}
# -{twine upload dist/*}
# -{pip install -e .}
"""
:copyright: (c) 2019 by K1DV5
:license: MIT, see LICENSE for more details.
"""

from setuptools import setup, find_packages

VERSION = '3.0.1'

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='docal',
    author="Kidus Adugna",
    author_email='kidusadugna@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Inject calculations into Word and LaTeX documents with ease!",
    entry_points={
        'console_scripts': [
            'docal=docal.__main__:main',
        ],
    },
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='docal, math, latex, word',
    packages=['docal', 'docal.parsers', 'docal.document'],
    url='https://github.com/K1DV5/docal',
    version=VERSION,
    zip_safe=False,
)
