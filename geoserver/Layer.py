# pylint: disable=W0212

"""
Layer
"""
import json
from geoserver.Resource import Resource
from geoserver.Style import Style


class Layer(Resource):
    """
    An object representing a GeoServer layer.

    :param name: The name of the workspace
    :param geoserver: The :class:`geoserver.GeoServer` instance this workspace belongs to.
    :param datastore: The datastore containing this layer.
    :param workspace: The workspace containing this layer.
    :type name: string
    :type geoserver: :class:`geoserver.GeoServer`
    :type workspace: :class:`geoserver.Workspace`
    :type datastore: :class:`geoserver.Datastore`
    """
    def __init__(self, name, geoserver, datastore, workspace):
        Resource.__init__(self, name, geoserver)
        self.datastore = datastore
        self.workspace = workspace

    def get_datastore(self):
        """
        Gets the datastore this layer belongs to.

        :return: The datastore containing this layer.
        :rtype: :class:`geoserver.Datastore`
        """
        return self.datastore

    def get_workspace(self):
        """
        Gets the workspace this layer belongs to.

        :return: The workspace containing this layer.
        :rtype: :class:`geoserver.Workspace`
        """
        return self.workspace

    def delete(self):
        """
        Deletes the layer from GeoServer.

        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        self.geoserver._request('layers/' + self.name, method='DELETE')
        self.geoserver.reload()

    def set_default_style(self, style):
        """
        Sets the default style for this layer.

        :param style: The style to set as default.
        :type style: string or :class:`geoserver.Style`
        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        :raise: :class:`ValueError` if the provided style is not valid.
        """
        name = style.get_name() if isinstance(style, Style) else style
        if not self.geoserver.get_style(name):
            raise ValueError('Invalid style: ' + name)
        base = self.geoserver.url
        layer_info = self.geoserver._get('layers/' + self.name)
        layer_info['layer']['defaultStyle']['name'] = name
        layer_info['layer']['defaultStyle']['href'] = base + 'styles/' + name
        self.geoserver._request(
            'layers/' + self.name, method='PUT',
            headers={'Content-type': 'application/json'},
            data=json.dumps(layer_info))

    def get_default_style(self):
        """
        Gets the default style for this layer.

        :return: The default style.
        :rtype: :class:`geoserver.Style`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        layer_info = self.geoserver._get('layers/' + self.name)['layer']
        return self.geoserver.get_style(layer_info['defaultStyle']['name'])
