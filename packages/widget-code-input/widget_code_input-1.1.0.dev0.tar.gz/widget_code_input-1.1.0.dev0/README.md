
# widget-code-input

[![Build Status](https://travis-ci.org/osscar-org/widget-code-input.svg?branch=master)](https://travis-ci.org/osscar-org/widget_code_input)
[![codecov](https://codecov.io/gh/osscar-org/widget-code-input/branch/master/graph/badge.svg)](https://codecov.io/gh/osscar-org/widget-code-input)


A widget to allow input of a python function, with syntax highlighting

## Try it live!

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/osscar-org/widget-code-input/master?urlpath=%2Flab%2Ftree%2Fexamples%2Fintroduction.ipynb)

## Installation

You can install using `pip`:

```bash
$ pip install widget_code_input
$ jupyter labextension enbale --py --sys-prefix widget_code_input
```

For a development installation (requires npm),

```bash
$ git clone https://github.com/osscar-org/widget-code-input.git
$ cd widget-code-input
$ pip install -e .
$ jupyter nbextension install --py --symlink --sys-prefix widget_code_input
$ jupyter nbextension enable --py --sys-prefix widget_code_input
$ jupyter labextension install .
```
