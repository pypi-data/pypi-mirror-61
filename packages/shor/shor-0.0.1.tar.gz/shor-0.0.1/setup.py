from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="shor",
    version="0.0.1",
    author="shor.dev",
    author_email="shordotdev@gmail.com",
    description="The Python Quantum Computing Library",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/shor-team/shor",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)