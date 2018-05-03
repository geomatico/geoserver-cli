# pylint: disable=W0212

"""
Style
"""
from geoserver.Resource import Resource


class Style(Resource):
    """
    An object representing a GeoServer style.

    :param name: The name of the style
    :param geoserver: The :class:`geoserver.GeoServer` instance this workspace belongs to.
    :type name: string
    :type geoserver: :class:`geoserver.GeoServer`
    """
    def __init__(self, name, geoserver):
        Resource.__init__(self, name, geoserver)

    def delete(self):
        """
        Deletes the style from GeoServer.

        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        self.geoserver._request('styles/' + self.name, method='DELETE')

    def set_sld(self, sld):
        """
        Sets the SLD content for this style.

        :param sld: SLD content to set.
        :type sld: string
        :rtype: None
        :raise: :class:`IOError` if any error occurs while requesting the REST API.
        """
        self.geoserver._request(
            'styles/' + self.name, method='PUT', extension='', data=sld,
            headers={'Content-type': 'application/vnd.ogc.sld+xml'})

    def get_sld(self):
        """
        Gets the SLD content for this style.

        :return: the SLD content.
        :rtype: string
        """
        style = self.geoserver._get('styles/' + self.name)
        return self.geoserver._request(
            'resource/styles/' + style['style']['filename'],
            extension='')

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.geoserver == other.geoserver and
                self.name == other.name)
