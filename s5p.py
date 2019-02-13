#!-*- coding: utf-8 -*-

"""
   To Download TROPOMI Product from s5phub

   @date: 2019.02.12
   @auth:ly
"""

import os
import base64
import requests


class s5p(object):
    def __init__(self, username=None, password=None, login_headers=None, login_data=None):
        """ Init s5p
        :param username: username
        :param password: password
        :param login_headers: browser headers for login s5phub
        :param login_data: form data for login s5phub
        """

        self.login_url = 'https://s5phub.copernicus.eu/dhus//login'
        self.product_url = 'https://s5phub.copernicus.eu/dhus/api/stub/products'
        self._username = username
        self._password = password
        self._login_headers = login_headers
        self._login_data = login_data


    def login(self):

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

        self._login_results = requests.post(self.login_url, headers=self._login_headers, data=self._login_data)


    def filter(self, platformname='Sentinel-5', producttype=None,
               processinglevel=None, processingmode=None, orbitnumber=None,
               beginPosition=None, endPosition=None, beginIngestionDate=None,
               endIngestionDate=None, offset=0, limit=25, sortedby='ingestiondate',
               order='desc', product_header=None, download=False, savepath=None):
        """

        :param platformname(str): satellites type, default Sentinel-5
        :param producttype(str): product type,
        :param processinglevel(str): product level, including Level1B and Level2, namely L1B and L2
        :param processingmode(str): including (Near real time) and (Offline)
        :param orbitnumber(int): satellites orbit number
        :param beginPosition(datetime.datetime):
        :param endPosition(datetime.datetime):
        :param beginIngestionDate(datetime.datetime):
        :param endIngestionDate(datetime.datetime):
        :param offset(int):
        :param limit(int): display the total numbers of file on one page, default 25
        :param sortedby(str): sorted type, including "ingestiondate", "beginposition" and "cloudcoverpercentage"
        :param order(str): order type, including "desc" and "asc"
        :param product_header(dict): browser headers to index product
        :param download(bool): logical to control if download file indexed
        :param savepath(str):
        :return:
        """

        self._download = download

        if savepath is None:
            savepath = ''
        self._savepath = savepath

        if product_header is None:
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
        else:
            self._product_header = product_header

        filters = ''

        if beginPosition is not None and endPosition is None:
            filters += '( beginPosition:[{0} TO NOW] ' \
                        'AND ' \
                        'endPosition:[{1} TO NOW] ) ' \
                        'AND '.format(beginPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     beginPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     )
        elif beginPosition is None and endPosition is not None:
            filters += '( beginPosition:[* TO {0}] ' \
                        'AND ' \
                        'endPosition:[* TO {1}] ) ' \
                        'AND '.format(endPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     endPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                     )
        elif beginPosition is not None and endPosition is not None:
            filters += '( beginPosition:[{0} TO {1}] ' \
                       'AND ' \
                       'endPosition:[{2} TO {3}] ) ' \
                       'AND '.format(beginPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                    endPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                    beginPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                    endPosition.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                    )

        if beginIngestionDate is not None and endIngestionDate is not None:
            filters += '( ingestionDate:[{0} TO {1} ] ) AND '.format(beginIngestionDate.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                                                    endIngestionDate.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                                                                    )
        elif beginIngestionDate is None and endIngestionDate is not None:
            filters += '( ingestionDate:[* TO {0} ] ) AND '.format(endIngestionDate.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        elif beginIngestionDate is not None and endIngestionDate is None:
            filters += '( ingestionDate:[{0} TO NOW ] ) AND '.format(beginIngestionDate.strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        mission = '(( platformname:{0} '.format(platformname)

        if processingmode is not None:
            mission += 'AND processingmode:{0} '.format(processingmode)

        if producttype is not None:
            mission += 'AND producttype:{0} '.format(producttype)

        if processinglevel is not None:
            mission += 'AND processinglevel:{0} '.format(processinglevel)

        if orbitnumber is not None:
            mission += 'AND orbitnumber:{0} '.format(orbitnumber)

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
                        'offset': offset,
                        'limit': limit,
                        'sortedby': sortedby,
                        'order': order
                        }

        self._filter_results = requests.get(self.product_url,
                                            headers=self._product_header,
                                            cookies=self._login_results.cookies,
                                            params=self._params)

        if self._download:
            self._parse_filters()

        return None

    def download(self):

        self._url = "https://s5phub.copernicus.eu/dhus/odata/v1/Products('{0}')//$value".format(self._uuid)

        with requests.get(self._url, headers=self._login_headers, stream=True) as r:
            if r.status_code == 200:
                with open(os.path.join(self._savepath, self._filename), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
            else:
                print('error!')


    def _parse_filters(self):

        self.json = self._filter_results.json()
        self.keys = self.json.keys()

        self.products = self.json.get('products', None)
        self._totalresults = self.json.get('totalresults', None)

        for iters in self.products:
            self._id = iters.get('id')
            self._uuid = iters.get('uuid')
            self._identifier = iters.get('identifier')
            self._footprint = iters.get('footprint')
            self._summary = iters.get('summary')
            self._filename = self._summary[1].split(':')[1].lstrip()
            self._Satellite = self._summary[4].split(':')[1].lstrip()
            self._size = self._summary[5].split(':')[1].lstrip()
            self._indexes = iters.get('indexes')

            product = self._indexes[1]
            self._generation_time = product.get('children')[1].get('value')
            self._ingesstion_time = product.get('children')[2].get('value')
            self._orbit_number_info = product.get('children')[4]
            self.revision_info = product.get('children')[11]

            self._thumbnail = iters.get('thumbnail')
            self._quicklook = iters.get('quicklook')
            self._instrument = iters.get('instrument')
            self._productType = iters.get('productType')
            self._itemClass = iters.get('itemClass')
            self._wkt = iters.get('wkt')
            self._offline = iters.get('offline')

            if self._download:
                print('Now, download {0}, filename total size {1}'.format(self._filename), self._size)
                self.download()

        return None

