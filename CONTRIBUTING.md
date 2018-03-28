# Contributing to Gello

First off, thanks for taking the time to contribute to Gello! :dog: :+1:

The following is a set of guidelines for contributing to Gello, which is hosted in the [Datadog Organization](https://github.com/datadog) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Python Styleguide](#python-styleguide)
  * [Documentation Styleguide](#documentation-styleguide)

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for Gello.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting A Bug Report

* Perform a search to see if the problem has already been reported. If the issue has been reported, **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). Create an issue on the Gello repository and provide the following information by filling in [the issue template](ISSUE_TEMPLATE.md).

### Pull Requests

* Fill in [the required template](PULL_REQUEST_TEMPLATE.md)
* Follow the [Python](#python-styleguide)styleguide
* End all files with a newline

## Styleguides

### Python Styleguide

All Python code must adhere to [PEP8 Standard Style](https://www.python.org/dev/peps/pep-0008/).

* All files, classes, and functions should have a docstring, following [Google's Docstring conventions](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html.

### Documentation Styleguide

* Eeach file must include the following header at the top of the file:

**For Python files**
```python
#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright {year} Datadog, Inc.
#
```

**For HTML files**
```html
<!--
  Unless explicitly stated otherwise all files in this repository are licensed
  under the Apache 2 License.

  This product includes software developed at Datadog
  (https://www.datadoghq.com/).

  Copyright {year} Datadog, Inc.
-->
```

* Each file, class, and method should have a docstring present.
* Use [Google Style Python Docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

#### Example

```python
def function_with_types_in_docstring(param1, param2):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.
    """
```
> Taken from [Example Google Style Python Docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
