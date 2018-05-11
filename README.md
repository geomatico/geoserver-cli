# geoserver-cli

## Setting up enviroment using virtualenvwrapper
First get your Python3 version
```bash
$ python3 -V
Python 3.6.3

```

use this version to create the virtualenv

```bash
$ mkvirtualenv geoserver-cli --python=python3.6
```

## Getting Started in dev mode

```bash
(geoserver-cli)$ pip install -r requirements.txt
(geoserver-cli)$ python setup.py develop
(geoserver-cli)$ geoserver
usage: geoserver [-h]
                 {ds,fonts,import,layer,layergroup,reload,reset,style,ws} ...

GeoServer CLI

optional arguments:
  -h, --help            show this help message and exit

Commands:
  {ds,fonts,import,layer,layergroup,reload,reset,style,ws}
    ds                  Manage datastores
    fonts               Show GeoServer's fonts
    import              Imports a file or directory.
    layer               Manage layers
    layergroup          Manage layer groups
    reload              Reload GeoServer
    reset               Reset GeoServer
    style               Manage styles
    ws                  Manage workspaces
```

## Test
To test the cli you'll be necessary a local geoserver instance running with the GEOSERVER_DATA_DIR pointing to the folder 
`geoserver-cli/test/geoserver_data_dir`. You can set your own GeoServer instance or, if you use Docker, you can run a 
geoserver instance ready to test running the next commands:

```bash
(geoserver-cli)$ make docker-run
(geoserver-cli)$ make test

```

## How to
* [Setting up and using Python3, Pip3, Virtualenv (for Python3) and Virtualenvwrapper (for Python3)](https://gist.github.com/IamAdiSri/a379c36b70044725a85a1216e7ee9a46)


