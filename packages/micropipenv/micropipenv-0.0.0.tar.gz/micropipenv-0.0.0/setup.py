from setuptools import setup


setup(
    name="micropipenv",
    version="0.0.0",
    description="A simple wrapper around pip to support Pipenv files",
    long_description="A simple wrapper around pip to support Pipenv files",
    author="Fridolin Pokorny",
    author_email="fridex.devel@gmail.com",
    license="GPLv3+",
    packages=[
        "micropipenv",
    ],
    package_data={"micropipenv": ["py.typed"]},
    entry_points={"console_scripts": ["micropipenv=micropipenv:cli"]},
)
