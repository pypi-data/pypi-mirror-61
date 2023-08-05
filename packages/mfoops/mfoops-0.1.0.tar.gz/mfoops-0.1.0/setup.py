import setuptools

setuptools.setup(
    name="mfoops",
    version="0.1.0",
    author="Matthew Farrellee",
    author_email="matt@cs.wisc.edu",
    descrption="Pseudorandom things",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mattf/mfoops",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
