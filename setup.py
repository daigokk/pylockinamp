from setuptools import setup, find_packages

setup(
    name='pylia',
    version='2.0.0',
    description='Python wrapper of LIA',
    author='daigokk',
    packages=['windows_only_package'],
    platforms=['Windows'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    install_requires=[
        numpy,
    ],
)
