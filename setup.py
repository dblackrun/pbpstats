from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pbpstats",
    version="1.3.1",
    author="Darryl Blackport",
    author_email="darryl.blackport@gmail.com",
    description="A package to scrape and parse NBA, WNBA and G-League play-by-play data",
    license="MIT License",
    keywords=["basketball", "NBA", "WNBA", "G-League", "play-by-play", "pbp"],
    url="https://github.com/dblackrun/pbpstats",
    packages=find_packages(),
    install_requires=["requests"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
