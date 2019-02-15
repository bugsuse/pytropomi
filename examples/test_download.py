#! -*- coding: utf-8 -*-

import os
from datetime import datetime

from shapely.geometry import Polygon

from downs5p import downs5p


products = ['L2__NO2___', 'L2__SO2___', 'L2__HCHO__', 'L2__O3____']

polygon = Polygon([(100, 20), (105, 25), (110, 30), (115, 35), (120, 30), (125, 25), (130, 20), (120, 15)])
area = 20

longitude = 121
latitude = 32

beginPosition = datetime(2019, 2, 1)
endPosition = datetime(2019, 2, 14)


def test_lonlat(longitude, latitude, beginPosition):
    for pro in products:
        savepath = '/root/works/tropomi/data/{0}'.format(pro.split('_')[2])
        os.system('mkdir {0}'.format(savepath))
        downs5p(producttype=pro, longitude=longitude, latitude=latitude, processingmode='Near real time',
                beginPosition=beginPosition, savepath=savepath)


def test_polygon(polygon, area, beginPosition):
    for pro in products:
        savepath = '/root/works/tropomi/data/{0}'.format(pro.split('_')[2])
        os.system('mkdir {0}'.format(savepath))
        downs5p(producttype=pro, polygon=polygon, area=area, processingmode='Near real time',
                beginPosition=beginPosition, savepath=savepath)

