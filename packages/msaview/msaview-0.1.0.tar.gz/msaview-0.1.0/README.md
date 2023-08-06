# msaview

[![Build Status](https://travis-ci.org/ostrokach/msaview.svg?branch=master)](https://travis-ci.org/ostrokach/msaview)
[![codecov](https://codecov.io/gh/ostrokach/msaview/branch/master/graph/badge.svg)](https://codecov.io/gh/ostrokach/msaview)

A set of Jupyter widgets useful for analyzing biological data.

## Installation

You can install using `pip`:

```bash
pip install msaview
```

Or if you use jupyterlab:

```bash
pip install msaview
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:

```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] msaview
```

## Development

Install the Python package using `pip`:

```bash
pip install -e .
```

Install the Javascript package using `jupyter` (not sure if you need to run `npm run build` first?):

```bash
jupyter labextension install .
```
