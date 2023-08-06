from setuptools import setup

import versioneer


setup(
    name="pummeler",
    author="Dougal J. Sutherland",
    author_email="dougal@gmail.com",
    url="https://github.com/dougalsutherland/pummeler/",
    packages=["pummeler"],
    package_data={"pummeler": ["data/*"]},
    entry_points={"console_scripts": ["pummel = pummeler.cli:main"]},
    description="Utilities for processing and analyzing ACS PUMS files.",
    install_requires=[
        "h5py",
        "numpy",
        "pandas>=0.21.0",
        "tables",
        "scipy",
        "scikit-learn",
        "tqdm",
    ],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="MIT",
    zip_safe=True,
)
