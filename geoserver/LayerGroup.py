# pylint: disable=W0212,C0301

"""
LayerGroup
"""
import json
from geoserver.Resource import Resource


class LayerGroup(Resource):
    """
    An object representing a GeoServer layer group.

    :param name: The name of the workspace
    :param geoserver: The :class:`geoserver.GeoServer` instance this workspace belongs to.
    :type name: string
    :type geoserver: :class:`geoserver.GeoServer`
    """

    def __init__(self, name, geoserver):
        Resource.__init__(self, name, geoserver)

    def delete(self):
        """
        Deletes the layer from GeoServer.

        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        self.geoserver._request('layergroups/' + self.name, method='DELETE')
        self.geoserver.reload()

    def set_layers(self, layers):
        """
        Sets the layers for this layer group.

        :param layers: Layers to add/remove to/from the group. Note that you don\'t need to specify all the layers. If the layer already exists in the group, it will be removed; if not it will be added.
        :type layers: list of string
        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        layergroup_info = self.geoserver._get('layergroups/' + self.name)
        published = layergroup_info['layerGroup']['publishables']['published']
        styles = layergroup_info['layerGroup']['styles']['style']

        def _unqualified(name):
            return name if ':' not in name else name.split(':')[1]

        # Add
        published_names = list(map(lambda p: p['name'], published))
        to_remove = []
        for layer in layers:
            if (layer not in published_names
                    and _unqualified(layer) not in published_names):
                published.append({
                    '@type': 'layer',
                    'name': layer
                })
                styles.append('null')
            else:
                to_remove.append(layer)

        # Remove
        unqualified_to_remove = list(map(_unqualified, to_remove))
        for i, layer in enumerate(published):
            name = layer['name']
            if ((':' in name and name in to_remove)
                    or (':' not in name and _unqualified(name) in unqualified_to_remove)):
                del published[i]
                del styles[i]

        self.geoserver._request(
            'layergroups/' + self.name, method='PUT',
            headers={'Content-type': 'application/json'},
            data=json.dumps(layergroup_info))

    def get_layers(self):
        """
        Gets all the layers composing this layer group.

        :return: a list of layers composing this group.
        :rtype: list of :class:`geoserver.Layer`
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        layergroup_info = self.geoserver._get(
            'layergroups/' + self.name)['layerGroup']
        published = layergroup_info['publishables']['published']
        layers_json = map(lambda l: self.geoserver._get(
            l['href'])['layer'], published)
        return list(map(self.geoserver._layer_from_json, layers_json))
