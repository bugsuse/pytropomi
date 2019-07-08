#! -*- coding: utf-8 -*-

from pytropomi.downs5p import downs5p


def test_lonlat(products, longitude, latitude, beginPosition, savepath=None):
    for pro in products:
        downs5p(producttype=pro, longitude=longitude, latitude=latitude, processingmode='Near real time',
                beginPosition=beginPosition, savepath=savepath)

def test_polygon1(products, polygon, area, savepath=None):
    for pro in products:
        downs5p(producttype=pro, polygon=polygon, area=area, processingmode='Near real time',
             savepath=savepath)


def test_polygon2(products, polygon, area, beginPosition, endPosition, savepath=None):
    for pro in products:
        downs5p(producttype=pro, polygon=polygon, area=area, processingmode='Near real time',
                beginPosition=beginPosition, endPosition=endPosition, savepath=savepath)

def test_polygon3(products, polygon, beginPosition, endPosition, savepath=None):
    for pro in products:
        downs5p(producttype=pro, polygon=polygon, processingmode='Near real time',
                beginPosition=beginPosition, endPosition=endPosition, savepath=savepath)

def test_polygon4(products, polygon, beginPosition, savepath=None):
    for pro in products:
        downs5p(producttype=pro, polygon=polygon, processingmode='Near real time',
                beginPosition=beginPosition, savepath=savepath)

def test_polygon5(products, polygon, endPosition, savepath=None):
    for pro in products:
        downs5p(producttype=pro, polygon=polygon, processingmode='Near real time',
                endPosition=endPosition, savepath=savepath)

def test_polygon6(products, polygon, endPosition, savepath):
    for pro in products:
        downs5p(producttype=pro, polygon=polygon, processingmode='Near real time',
                endPosition=endPosition, savepath=savepath)

def test_polygon7(products, polygon, endPosition, savepath):
    for pro in products:
        downs5p(producttype=pro, polygon=polygon, processingmode='Offline',
                endPosition=endPosition, savepath=savepath)

def test_polygon8(products, polygon, endPosition, savepath):
    for pro in products:
        downs5p(producttype=pro, polygon=polygon, processingmode='Reprocessing',
                endPosition=endPosition, savepath=savepath)


if __name__=='__main__':

    import os
    from datetime import datetime
    from shapely.geometry import Polygon

    products = ['L2__NO2___', 'L2__SO2___', 'L2__HCHO__', 'L2__O3____']

    polygon = Polygon([(100, 20), (105, 25), (110, 30), (115, 35), (120, 30), (125, 25), (130, 20), (120, 15)])
    area = 20

    longitude = 121
    latitude = 32

    beginPosition = datetime(2019, 7, 7)
    endPosition = datetime(2019, 7, 8)

    savepath = './test'

    test_polygon1(products, polygon, area, savepath=None) 

