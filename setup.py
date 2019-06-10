# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


def get_metadata(relpath, varname):
    """Read metadata info from a file without importing it."""
    from os.path import dirname, join

    if "__file__" not in globals():
        root = "."
    else:
        root = dirname(__file__)

    for line in open(join(root, relpath), "rb"):
        line = line.decode("cp437")
        if varname in line:
            if '"' in line:
                return line.split('"')[1]
            elif "'" in line:
                return line.split("'")[1]


setup(
    name="customxepr",
    version=get_metadata("customxepr/main.py", "__version__"),
    description="Python interface for for Bruker Xepr.",
    url=get_metadata("customxepr/main.py", "__url__"),
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
                    "gui/*.ui",
                    "experiment/*.txt",
            ],
    },
    data_files=[('customxepr_info', ['README.md', 'CHANGELOG.md'])],
    install_requires=[
                "decorator",
                "future",
                "ipython",
                "keithley2600>=1.2.1",
                "keithleygui>=1.1.2",
                "pyvisa",
                "pyvisa-py",
                "pyqtgraph_cx",
                "lmfit",
                "matplotlib",
                "markdown2",
                "numpy",
                "pygments",
                "PySignal",
                "qtpy",
                "qtconsole",
                "configparser;python_version<='2.7'",
                "scipy",
                "mercuryitc@git+https://github.com/OE-FET/mercuryitc",
                "mercurygui@git+https://github.com/OE-FET/mercurygui",
    ],
    zip_safe=False,
    entry_points={
      "console_scripts": ["CustomXepr=customxepr.startup:run"],
      },
    )
