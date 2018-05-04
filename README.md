# geoserver-cli

## Getting Started in dev mode

```bash
(geoserver-cli)$ pip install -r requirements.txt
(geoserver-cli)$ python setup.py install

```

## Test
To test the cli you'll be necessary a local geoserver instance running with the GEOSERVER_DATA_DIR pointing to the folder 
`geoserver-cli/test/geoserver_data_dir`. You can set your own GeoServer instance or, if you use Docker, you can run a 
geoserver instance ready to test running the next commands:

```bash
(geoserver-cli)$ make docker-run
(geoserver-cli)$ make test

```

