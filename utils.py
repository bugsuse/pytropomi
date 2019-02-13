#!-*- coding: utf-8 -*-


import shapely.wkt
from shapely.geometry import Point


def inpolygon(wkt, longitude, latitude):

    multipolygon = shapely.wkt.loads(wkt)
    point = Point(longitude, latitude)

    return multipolygon.contains(point), multipolygon

