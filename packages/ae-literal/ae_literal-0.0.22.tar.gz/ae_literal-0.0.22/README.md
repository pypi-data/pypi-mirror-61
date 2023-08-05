<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
  All changes will be deployed automatically to all the portions of this namespace package.
-->
# literal portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_literal/master?logo=python)](
    https://gitlab.com/ae-group/ae_literal)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_literal)](
    https://pypi.org/project/ae-literal/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes for to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_literal/coverage.svg)](
    https://ae-group.gitlab.io/ae_literal/coverage/ae_literal_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_literal/mypy.svg)](
    https://ae-group.gitlab.io/ae_literal/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_literal/pylint.svg)](
    https://ae-group.gitlab.io/ae_literal/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_literal)](
    https://pypi.org/project/ae-literal/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_literal)](
    https://pypi.org/project/ae-literal/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_literal)](
    https://pypi.org/project/ae-literal/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_literal)](
    https://pypi.org/project/ae-literal/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_literal)](
    https://libraries.io/pypi/ae-literal)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_literal)](
    https://pypi.org/project/ae-literal/#files)


## installation

Execute the following command for to use the ae.literal module in your
application. It will install ae.literal into your python (virtual) environment:
 
```shell script
pip install ae-literal
```

If you instead want to contribute to this portion then first fork
[the ae-literal repository at GitLab](https://gitlab.com/ae-group/ae_literal "ae.literal code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_literal):

```shell script
pip install -e .[dev]
```

The last command will install this module portion into your virtual environment, along with
the tools you need to develop and run tests or for to extend the portion documentation.
For to contribute only to the unit tests or the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

More info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.literal.html#module-ae.literal
"ae_literal documentation").

<!-- Common files version 0.0.34 deployed (with 0.0.34)
     to the ae_literal module version 0.0.20.
-->