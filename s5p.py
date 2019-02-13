#!-*- coding: utf-8 -*-

"""
   To Download TROPOMI Product from s5phub

   @date: 2019.02.12
   @auth:ly
"""

"""
    TODO:
    * 选择只包含给定点的文件
    * 选择包含给定区域的文件
    * 调整文件下载策略
    * 支持多线程下载
    
"""


import os
import base64
import warnings

import requests
from shapely import wkt
from shapely.geometry import Point


class s5p(object):
    def __init__(self, username=None, password=None, login_headers=None, login_data=None, platformname='Sentinel-5',
                 producttype=None, processinglevel=None, processingmode=None, orbitnumber=None, beginPosition=None,
                 endPosition=None, beginIngestionDate=None, endIngestionDate=None, offset=0, limit=25,
                 sortedby='ingestiondate', order='desc', product_header=None):
        """ Init s5p
        :param username: username, default username is s5pguest
        :param password: password, default password is s5pguest
        :param login_headers: browser headers for login s5phub
        :param login_data: form data for login s5phub
        :param platformname(str): satellites type, default Sentinel-5
        :param producttype(str): product type,
        :param processinglevel(str): product level, including Level1B and Level2, namely L1B and L2
        :param processingmode(str): including (Near real time) and (Offline)
        :param orbitnumber(int): satellites orbit number
        :param beginPosition(datetime.datetime):
        :param endPosition(datetime.datetime):
        :param beginIngestionDate(datetime.datetime):
        :param endIngestionDate(datetime.datetime):
        :param offset(int): skip the number of file, 从开头跳过多少个文件
        :param limit(int): display the total numbers of file on one page, default 25，每页显示的文件数
        :param sortedby(str): sorted type, including "ingestiondate", "beginposition" and "cloudcoverpercentage"
        :param order(str): order type, including "desc" and "asc"，降序和升序
        :param product_header(dict): browser headers to index product
        """

        self._login_url = 'https://s5phub.copernicus.eu/dhus//login'
        self._product_url = 'https://s5phub.copernicus.eu/dhus/api/stub/products'
        self._username = username
        self._password = password
        self._login_headers = login_headers
        self._login_data = login_data
        self._platformname = platformname
        self._producttype = producttype
        self._processinglevel = processinglevel
        self._processingmode = processingmode
        self._orbitnumber = orbitnumber
        self._beginPosition = beginPosition
        self._endPosition = endPosition
        self._beginIngestionDate = beginIngestionDate
        self._endIngestionDate = endIngestionDate
        self._offset = offset
        self._limit = limit
        self._sortedby = sortedby
        self._order = order
        self._product_header = product_header


    def login(self):
        """login s5phub
        """

        if self._username is None and self._password is None:
            self._username, self._password = 's5pguest', 's5pguest'
        else:
            raise ValueError('username: {0} \npassword: {1}\n'.format(self._username, self._password))

        self._login_data = {'login_username': self._username,
                            'login_password': self._password}

        if self._login_headers is None:
            self._login_headers = {'Accept': 'application/json, text/plain, */*',
                                   'Accept-Encoding': 'gzip, deflate, br',
                                   'Accept-Language': 'zh-CN,zh;q=0.9',
                                   'Authorization': 'Basic {0}'.format(base64.b64encode((self._username +
                                                                                        ':' +
                                                                                        self._password).encode('utf-8')).decode('utf-8')),
                                   'Cache-Control': 'no-cache',
                                   'Connection': 'keep-alive',
                                   'Content-Type': 'application/x-www-form-urlencoded',
                                   'Host': 's5phub.copernicus.eu',
                                   'Origin': 'https://s5phub.copernicus.eu',
                                   'Pragma': 'no-cache',
                                   'Referer': 'https://s5phub.copernicus.eu/dhus/',
                                   'User-Agent': 'Mozilla/5.0 (Macintosh; '
                                                 'Intel Mac OS X 10_13_6) '
                                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                 'Chrome/71.0.3578.98 '
                                                 'Safari/537.36',
                                   'X-Requested-With': 'XMLHttpRequest'
                                   }

        self._login_results = requests.post(self._login_url, headers=self._login_headers, data=self._login_data)

        if self._login_results.status_code == 200:
            print('login successfully!')
        else:
            print('status code is {0}'.format(self._login_results.status_code))


    def filter(self):
        """
        :return:
        """

        if self._product_header is None:
            self._product_header = {'Accept': 'application/json, text/plain, */*',
                                  'Accept-Encoding': 'gzip, deflate, br',
                                  'Accept-Language': 'zh-CN,zh;q=0.9',
                                  'Cache-Control': 'no-cache',
                                  'Connection': 'keep-alive',
                                  'Host': 's5phub.copernicus.eu',
                                  'Pragma': 'no-cache',
                                  'Referer': 'https://s5phub.copernicus.eu/dhus/',
                                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)'
                                                ' AppleWebKit/537.36 (KHTML, like Gecko) '
                                                'Chrome/71.0.3578.98 '
                                                'Safari/537.36',
                                  'X-Requested-With': 'XMLHttpRequest'}

        filters = ''

        if self._beginPosition is not None and self._endPosition is None:
            filters += '( beginPosition:[{0} TO NOW] ' \
                        'AND ' \
                        'endPosition:[{1} TO NOW] ) ' \
                        'AND '.format(self._beginPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     self._beginPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     )
        elif self._beginPosition is None and self._endPosition is not None:
            filters += '( beginPosition:[* TO {0}] ' \
                        'AND ' \
                        'endPosition:[* TO {1}] ) ' \
                        'AND '.format(self._endPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                      self._endPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     )
        elif self._beginPosition is not None and self._endPosition is not None:
            filters += '( beginPosition:[{0} TO {1}] ' \
                       'AND ' \
                       'endPosition:[{2} TO {3}] ) ' \
                       'AND '.format(self._beginPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     self._endPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     self._beginPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     self._endPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                    )

        if self._beginIngestionDate is not None and self._endIngestionDate is not None:
            filters += '( ingestionDate:[{0} TO {1} ] ) AND '.format(self._beginIngestionDate.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                                                     self._endIngestionDate.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                                                    )
        elif self._beginIngestionDate is None and self._endIngestionDate is not None:
            filters += '( ingestionDate:[* TO {0} ] ) AND '.format(self._endIngestionDate.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        elif self._beginIngestionDate is not None and self._endIngestionDate is None:
            filters += '( ingestionDate:[{0} TO NOW ] ) AND '.format(self._beginIngestionDate.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        mission = '(( platformname:{0} '.format(self._platformname)

        if self._processingmode is not None:
            mission += 'AND processingmode:{0} '.format(self._processingmode)

        if self._producttype is not None:
            mission += 'AND producttype:{0} '.format(self._producttype)

        if self._processinglevel is not None:
            mission += 'AND processinglevel:{0} '.format(self._processinglevel)

        if self._orbitnumber is not None:
            mission += 'AND orbitnumber:{0} '.format(self._orbitnumber)

        mission += ' ) )'

        self._filters = filters
        self._mission = mission

        if len(filters) == 0:
            if len(mission) <=30:
                filters = '*'
            elif len(mission) > 30:
                filters += mission
        else:
            if len(mission) > 30:
                filters = filters + mission

        self._params = {'filter': filters,
                        'offset': self._offset,
                        'limit': self._limit,
                        'sortedby': self._sortedby,
                        'order': self._order
                        }

        return requests.get(self._product_url,
                            headers=self._product_header,
                            cookies=self._login_results.cookies,
                            params=self._params)


    def next_page(self, offset=None):
        """
        :param offset:
        :return:
        """
        if offset is not None:
            self._offset = offset

        return self.filter()


    def parse_filters(self, longitude=None, latitude=None):

        self.json = self.filter.json()
        self.keys = self.json.keys()

        self.products = self.json.get('products', None)
        self.totalresults = self.json.get('totalresults', None)

        for iters in self.products:
            self._id = iters.get('id')
            self._uuid = iters.get('uuid')
            self._identifier = iters.get('identifier')
            self._footprint = iters.get('footprint')
            self._summary = iters.get('summary')
            self._filename = self._summary[1].split(':')[1].lstrip()
            self._satellite = self._summary[4].split(':')[1].lstrip()
            self._size = self._summary[5].split(':')[1].lstrip()
            self._indexes = iters.get('indexes')

            product = self._indexes[1]
            self._generation_time = product.get('children')[1].get('value')
            self._ingesstion_time = product.get('children')[2].get('value')
            self._orbit_number_info = product.get('children')[4]
            self._revision_info = product.get('children')[11]

            self._thumbnail = iters.get('thumbnail')
            self._quicklook = iters.get('quicklook')
            self._instrument = iters.get('instrument')
            self._productType = iters.get('productType')
            self._itemClass = iters.get('itemClass')
            self._wkt = iters.get('wkt')
            self._offline = iters.get('offline')

            if longitude is not None and latitude is not None:
                self._multipolygon = wkt.loads(self._wkt)
                point = Point(longitude, latitude)

                if self._multipolygon.contains(point):
                    pass
            else:
                return None

    def download(self, uuid, savepath=None, chunk_size=1024):

        if savepath is None:
            savepath = ''
        self._savepath = savepath

        self._url = "https://s5phub.copernicus.eu/dhus/odata/v1/Products('{0}')//$value".format(uuid)

        with requests.get(self._url, headers=self._login_headers, stream=True) as r:
            if r.status_code == 200:
                with open(os.path.join(self._savepath, self._filename), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
            else:
                warnings.warn('warning', '{0} download failed, http status code: {1}'.format(self._filename,
                                                                                             r.status_code))
