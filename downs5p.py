#!-*- coding: utf-8 -*-

from s5p import s5p


def downs5p(username=None, password=None, login_headers=None, login_data=None, platformname='Sentinel-5',
            producttype=None, processinglevel=None, processingmode=None, orbitnumber=None, beginPosition=None,
            endPosition=None, beginIngestionDate=None, endIngestionDate=None, offset=0, limit=25,
            sortedby='ingestiondate', order='desc', product_header=None, longitude=None, latitude=None,
            polygon=None, area=None, savepath=None, chunk_size=1024):
    """
    :param username:
    :param password:
    :param login_headers:
    :param login_data:
    :param platformname:
    :param producttype:
    :param processinglevel:
    :param processingmode:
    :param orbitnumber:
    :param beginPosition:
    :param endPosition:
    :param beginIngestionDate:
    :param endIngestionDate:
    :param offset:
    :param limit:
    :param sortedby:
    :param order:
    :param product_header:
    :param longitude:
    :param latitude:
    :param polygon:
    :param area:
    :param savepath:
    :param chunk_size:
    :return:
    """

    sp = s5p(username=username, password=password, login_headers=login_headers, login_data=login_data,
             platformname=platformname, producttype=producttype, processinglevel=processinglevel,
             processingmode=processingmode, orbitnumber=orbitnumber, offset=offset, limit=limit,
             sortedby=sortedby, order=order, product_header=product_header)

    login = sp.login()

    if login:
        print('login successfully!')

    sf = sp.search(polygon=polygon, area=area, longitude=longitude, latitude=latitude)

    print('The total number of file indexed is {0}.'.format(sp.totalresults))

    for i in range(1, sp.totalresults/sp._limit):
        for sg in sf:
            if len(list(sf)) > 0:
                print('Now, download {0}, the total size of file is {1}.'.format(sg[2], sg[3]))
                sp.download(sg[1], sg[2])
            else:
                print('No indexed file!')

            print('Now, indexed new page...')
            sf = sp.next_page(offset=i * sp._limit)


if __name__=='__main__':
    downs5p(producttype='L2__NO2___', longitude=121, latitude=32)
