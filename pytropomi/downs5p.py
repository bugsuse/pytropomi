#!-*- coding: utf-8 -*-

from .s5p import s5p


def downs5p(username=None, password=None, login_headers=None, login_data=None, platformname='Sentinel-5',
            producttype=None, processinglevel=None, processingmode=None, orbitnumber=None, beginPosition=None,
            endPosition=None, beginIngestionDate=None, endIngestionDate=None, offset=0, limit=25,
            sortedby='ingestiondate', order='desc', product_header=None, longitude=None, latitude=None,
            polygon=None, area=None, savepath=None, chunk_size=1024):
    """
    :param username: username, default username is s5pguest
    :param password: password, default password is s5pguest
    :param login_headers: browser headers for login s5phub
    :param login_data: form data for login s5phub
    :param product_header(dict): browser headers to index product
    :param platformname(str): satellites type, default Sentinel-5
    :param producttype(str): product type, Level 2 include L2__NO2___, L2__SO2___, L2__O3____ etc, please see tropomi
                           to get the details product type list
    :param processinglevel(str): product level, including Level1B and Level2, i.e. L1B and L2
    :param processingmode(str): including (Near real time) and (Offline)
    :param orbitnumber(int): satellites orbit number
    :param beginPosition(datetime.datetime): the start date for indexing product file
    :param endPosition(datetime.datetime): the end date for indexing product file
    :param beginIngestionDate(datetime.datetime): the ingestion begin date for indexing product file
    :param endIngestionDate(datetime.datetime): the ingestion end date for indexing product file
    :param offset(int): the number of file needing skip
    :param limit(int): display the total numbers of file on indexed page, default 25
    :param sortedby(str): sorted type, optional parameters include "ingestiondate", "beginposition" and "cloudcoverpercentage"
    :param order(str): order type, optional parameters include "desc" and "asc"，i.e. descending or ascending
    :param longitude(float): the longitude use to determine whether the coordinate within the orbit
    :param latitude(float): the latitude use to determine whether the coordinate within the orbit
    :param polygon(Polygon): the polygon use to determine whether the polygon intersect with the orbit
    :param area(float): the min value of area use to filter the polygon intersected with the orbit
    :param savepath(str): the path saved product file
    :param chunk_size(int): the size of chunk write to file
    :return:
    """

    sp = s5p(username=username, password=password, login_headers=login_headers, login_data=login_data,
             platformname=platformname, producttype=producttype, processinglevel=processinglevel,
             beginPosition=beginPosition, endPosition=endPosition, beginIngestionDate=beginIngestionDate,
             endIngestionDate=endIngestionDate, processingmode=processingmode, orbitnumber=orbitnumber,
             offset=offset, limit=limit, sortedby=sortedby, order=order, product_header=product_header)

    login = sp.login()

    if login:
        print('login successfully!')

    sfs = list(sp.search(polygon=polygon, area=area, longitude=longitude, latitude=latitude))

    print('The total number of file indexed is {0}.'.format(sp.totalresults))

    for i in range(1, int(sp.totalresults/sp._limit)):
        for sg in sfs:
            print('Now, download {0}, the total size of file is {1}.'.format(sg[2], sg[3]))
            sp.download(sg[1], filename=sg[2], savepath=savepath, chunk_size=chunk_size)

        print('Now, indexed new page {0}...'.format(i+1))
        sfs = sp.next_page(offset=i*sp._limit)
