from setuptools import setup, find_packages

setup(
    name='pylia',
    version='2.0.0',
    description='Python wrapper of LIA',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='daigokk',
    url='https://github.com/daigokk/pylia',
    packages=find_packages(),
    include_package_data=True,  # MANIFEST.in に従って追加ファイルを含める
    package_data={
        'pylia': ['pylia/bin/lia.exe'],  # バイナリを含める
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
