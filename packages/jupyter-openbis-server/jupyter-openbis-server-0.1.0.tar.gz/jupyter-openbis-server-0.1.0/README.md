# Jupyter openBIS Server


The server part of the `jupyter-openbis-extension` and `jupyterlab-openbis` notebook extension. Uses the `pyBIS` module internally to communicate with openBIS. Communicates with the notebook extensions via the tornado webserver.

## Install the server extension

The server extension will be automatically installed when you install the Jupyter Notebook Extension (the «classic» Jupyter Notebook):

```
pip install --upgrade jupyter-openbis-extension
```

If you need to install or upgrade the server extension alone, you can do so by:

```
pip install --upgrade jupyter-openbis-server
```

## install Jupyter extension manually

In most cases, a simple `pip install --upgrade jupyter-openbis-server` will install the server extension. However, in some cases (e.g. when installing via `pip install -e .`) you need to issue the following command to register the extension:

```
$ jupyter serverextension enable --py jupyter-openbis-server
```

This will create a file `~/.jupyter/jupyter_notebook_config.json` with the following content:

```
{
  "NotebookApp": {
    "nbserver_extensions": {
      "jupyter-openbis-server.main": true
    }
  }
}
```

## Uninstall Jupyter openBIS Server

Unfortunately, `pip` doesn't automatically clean up the Jupyter configuration when uninstalling. You have to do it yourself:

```
$ jupyter serverextension disable --py jupyter-openbis-server
$ pip uninstall jupyter-openbis-server
```