import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PYRMC",
    version="2.0.1",
    author="pyslow_riding",
    author_email="slowridingytb@gmail.com",
    description="console line tool to add function to be independent!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)