#!-*- coding: utf-8 -*-

import shapely.wkt
import shapely.geometry


def inpolygon(wkt, longitude, latitude):
    """ To determine whether the longitude and latitude coordinate is within the orbit
    :param wkt(str): the orbit wkt info
    :param longitude: to determine whether the longitude within the orbit
    :param latitude: to determine whether the latitude within the orbit
    :return: logical value whether the coordinate within the orbit and multipolygon
    """

    multipolygon = shapely.wkt.loads(wkt)
    point = shapely.geometry.Point(longitude, latitude)

    return multipolygon.contains(point), multipolygon

def polygonits(wkt, polygon, area):
    """ To determine whether the polygon intersect with the orbit
    :param wkt(str): the orbit wkt info
    :param polygon(Polygon): to determine whether the polygon intersect with the orbit
    :param area(float): the min area to filter the polygon intersect with the orbit
    :return: logical value whether the polygon intersect with the orbit
    """

    if area is None:
        area = 0

    multipolygon = shapely.wkt.loads(wkt)

    its = multipolygon.intersection(polygon)

    if its.area > area:
        return True, its
    else:
        return False, its
