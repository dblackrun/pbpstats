from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pbpstats',
    version='0.0.8',
    author='Darryl Blackport',
    author_email='darryl.blackport@gmail.com',
    description='A package to scrape and parse NBA, WNBA and G-League play-by-play data',
    license='MIT License',
    keywords=['basketball', 'NBA', 'WNBA', 'G-League', 'play-by-play', 'pbp'],
    url='https://github.com/dblackrun/pbpstats',
    packages=['pbpstats'],
    install_requires=['requests'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
