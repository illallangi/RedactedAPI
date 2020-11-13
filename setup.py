import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="illallangi-redactedapi",
    version="0.0.1",
    author="Andrew Cole",
    author_email="andrew.cole@illallangi.com",
    description="TODO: SET DESCRIPTION",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/illallangi/RedactedAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['redacted-tool=illallangi.redacted:__main__.cli'],
    },
    install_requires=[
        'click',
        'diskcache',
        'loguru',
        'notifiers',
        'requests',
        'yarl',
    ]
)
