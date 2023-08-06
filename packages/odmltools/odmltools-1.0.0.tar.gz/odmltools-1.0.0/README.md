![Travis build](https://travis-ci.org/G-Node/odmltools.svg?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/oo5lxr6h4pfc9ly7/branch/master?svg=true)](https://ci.appveyor.com/project/G-Node/odmltools/branch/master)
![Test coverage](https://coveralls.io/repos/github/G-Node/odmltools/badge.svg?branch=master)

# odmltools

odmltools is a package collecting convenience scripts for the odML python-project.
The Python odML library is available on [GitHub](https://github.com/G-Node/python-odml).

The open metadata Markup Language is a file based format (XML, JSON, YAML) for storing
metadata in an organised human- and machine-readable way. odML is an initiative to define
and establish an open, flexible, and easy-to-use format to transport metadata.

# Convenience scripts

Currently the package contains a convenience script to import DataCite XML files to odML: 

The script is automatically installed and available via the command line. It provides 
detailed usage descriptions by adding the `help` flag to the command.

    odmlimportdatacite -h

# Building from source

To download the odmltools library please either use git and clone
the repository from GitHub:

```
  $ git clone https://github.com/G-Node/odmltools.git
```

If you don't want to use git download the ZIP file also provided on
GitHub to your computer (e.g. as above on your home directory under a "toolbox"
folder).

To install the Python-odML library, enter the corresponding directory and run:

```
  $ cd odmltools
  $ python setup.py install
```

# Documentation

More information about the project including related projects as well as tutorials and
examples can be found at our [odML project page](https://g-node.github.io/python-odml).

# Bugs & Questions

Should you find a behaviour that is likely a bug or feel there is something missing,
just create an issue over at the GitHub [odmltools issue tracker](
https://github.com/G-Node/odmltools/issues).
