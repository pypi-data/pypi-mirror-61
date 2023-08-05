import setuptools
install_requires = [
    "click",
    "google-cloud-storage",
    "google-cloud-scheduler",
    "halo",
    "papermill",
    "jupyter-repo2docker",
    "jupyter",
    "colorama",
    "ipykernel",
    "gcsfs",
    "pandas",
    "pathlib",
    "timeago"
]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="treebeard",
    version="0.0.25",
    author="Treebeard Technologies",
    author_email="alex@treebeard.io",
    description="Tools for notebook hosting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={'treebeard': ['deploy/*', 'treebeard']},
    entry_points={"console_scripts": ["treebeard = treebeard.treebeard:cli"]},
    install_requires=install_requires,
)
