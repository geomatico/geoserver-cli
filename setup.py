from distutils.core import setup
import setuptools

setup(
    name='geoserver-cli',
    packages=['geoserver/cli'],
    version='0.1.0',
    description='GeoServer CLI',
    author='geomati.co',
    author_email='info@geomati.co',
    url='https://github.com/geomatico/geoserver-cli',
    download_url='https://github.com/geomatico/geoserver-cli/archive/0.1.0.tar.gz',
    keywords=['geomatico', 'geoserver', 'cli'],
    classifiers=[],
    scripts=['geoserver/cli/geoserver'],
    install_requires=[]
)
