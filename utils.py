#!-*- coding: utf-8 -*-

import shapely.wkt
import shapely.geometry


def inpolygon(wkt, longitude, latitude):
    """
    :param wkt:
    :param longitude:
    :param latitude:
    :return:
    """

    multipolygon = shapely.wkt.loads(wkt)
    point = shapely.geometry.Point(longitude, latitude)

    return multipolygon.contains(point), multipolygon

def polygonits(wkt, polygon, area):
    """
    :param wkt:
    :param polygon:
    :param area:
    :return:
    """

    if area is None:
        area = 0

    if ~isinstance(polygon, shapely.geometry.polygon.Polygon):
        raise ValueError('The type of variable polygon must be shapely.geometry.polygon.Polygon!')

    multipolygon = shapely.wkt.loads(wkt)

    its = multipolygon.intersection(polygon)

    if its.area > area:
        return True, its
