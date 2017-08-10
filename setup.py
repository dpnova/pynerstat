from setuptools import find_packages, setup

classifiers = [
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Framework :: Twisted",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
]

if __name__ == "__main__":

    with open('README.md') as f:
        readme = f.read()

    setup(
        name="minerstat",
        packages=find_packages('.'),
        package_dir={"": "."},
        setup_requires=[],
        install_requires=[
            "six",
            "Twisted[tls] >= 16.4.0",
            "attrs",
        ],
        extras_require={
            "dev": [
                "mock",
                "pep8",
                "sphinx",
                "flake8",
                "flake8-mypy"
            ],
        },
        author="David Novakovic",
        author_email="dpn@dpn.name",
        classifiers=classifiers,
        description="A fully featured client for minerstat.com",
        license="Apache 2.0",
        url="https://github.com/dpnova/minerstat",
        long_description=readme,
        scripts=['bin/minerstat']
    )
