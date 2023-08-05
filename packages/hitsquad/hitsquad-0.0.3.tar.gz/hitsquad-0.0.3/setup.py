import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.readlines()

setuptools.setup(
    name="hitsquad",
    version="0.0.3",
    author="Shubham Arawkar",
    author_email="arawkar.shubham08@gmail.com",
    description="GGWP command broadcast over ssh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "hitsquad = hitsquad.hitsquad:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.5',
)
