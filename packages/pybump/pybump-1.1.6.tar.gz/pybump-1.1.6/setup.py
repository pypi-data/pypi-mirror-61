import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

keywords = ['bump', 'version', 'appVersion', 'versioning', 'helm', 'charts', 'setup.py', 'promote']

setuptools.setup(
    name="pybump",
    version="1.1.6",
    author="Arie Lev",
    author_email="levinsonarie@gmail.com",
    description="Python version bumper",
    keywords=keywords,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/ArieLevs/PyBump",
    license='Apache License 2.0',
    packages=setuptools.find_packages(),
    install_requires=[
        'pyyaml==5.1',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'pybump = pybump.pybump:main'
        ],
    },
)
