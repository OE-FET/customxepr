# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="customxepr",
    version="v3.1.2.dev1",
    description="Python interface for for Bruker Xepr.",
    url="https://github.com/OE-FET/customxepr",
    author="Sam Schott",
    author_email="ss2151@cam.ac.uk",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        "customxepr": [
            "gui/resources/*.icns",
            "gui/resources/*.png",
            "gui/resources/*.md",
            "gui/resources/*.ui",
            "gui/*.ui",
            "experiment/*.txt",
        ],
    },
    install_requires=[
        "decorator",
        "ipython",
        "keithley2600>=1.2.1",
        "keithleygui>=1.1.2",
        "pint",
        "pyvisa",
        "pyvisa-py",
        "lmfit",
        "markdown2",
        "numpy",
        "pygments",
        "PySignal",
        "PyQt5",
        "qtconsole",
        'configparser;python_version<="2.7"',
        "scipy",
        "mercuryitc>=0.2.1",
        "mercurygui>=2.0.0",
        "XeprAPI"
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": ["customxepr=customxepr.startup:run_gui"],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
