import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='simar_co6_101703543', # Replace with your own username
    version="0.0.1",
    author="Simarpreet Singh",
    author_email="sgulati_be17@thapar.edu",
    description="A small package that showcases topsis approach",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simargulati/simar_coe6_101703543",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)