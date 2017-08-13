from setuptools import setup
import os
from setuptools.command.install import install


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


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


ms_extra_files = package_files('minerstat/clients')
tw_extra_files = package_files('twisted')


try:
    import twisted  # noqa
except ImportError:
    raise SystemExit("twisted not found.  Make sure you "
                     "have installed the Twisted core package.")


class InstallTwistedPlugin(install, object):
    def run(self):
        super(InstallTwistedPlugin, self).run()

        # Make Twisted regenerate the dropin.cache, if possible.  This is necessary
        # because in a site-wide install, dropin.cache cannot be rewritten by
        # normal users.
        print("Attempting to update Twisted plugin cache.")
        try:
            from twisted.plugin import IPlugin, getPlugins
            list(getPlugins(IPlugin))
            print("Twisted plugin cache updated successfully.")
        except Exception as e:
            print("*** Failed to update Twisted plugin cache. ***")
            print(str(e))


try:
    from setuptools.command import egg_info
    egg_info.write_toplevel_names
except (ImportError, AttributeError):
    pass
else:
    def _top_level_package(name):
        return name.split('.', 1)[0]

    def _hacked_write_toplevel_names(cmd, basename, filename):
        pkgs = dict.fromkeys(
            [
                _top_level_package(k)
                for k in cmd.distribution.iter_distribution_names()
                if _top_level_package(k) != "twisted"
            ]
        )
        cmd.write_file("top-level names", filename, '\n'.join(pkgs) + '\n')

    egg_info.write_toplevel_names = _hacked_write_toplevel_names


if __name__ == "__main__":

    with open('README.md') as f:
        readme = f.read()

    setup(
        name="minerstat",
        packages=[
            "minerstat",
            "minerstat.miners",
            "twisted.plugins"
        ],
        package_data={
            'minerstat': ms_extra_files,
            'twisted': tw_extra_files
        },
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
        scripts=['bin/minerstat'],
        cmdclass={
            'install': InstallTwistedPlugin,
        }
    )
