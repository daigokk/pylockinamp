from setuptools import setup, find_packages

setup(
    name='pylia',
    version='2.0.0',
    description='Python wrapper of LIA',
    author='daigokk',
    packages=['windows_only_package'],
    platforms=['Windows'],
    include_package_data=True,  # MANIFEST.in に従って追加ファイルを含める
    package_data={
        'pylia': ['bin/lia.exe'],  # バイナリを含める
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    install_requires=[
        'numpy',
    ],
)
