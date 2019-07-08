# pytropomi
This python module is to download Sentinel-5 from s5phub data center of [TROPOMI](http://www.tropomi.eu), and now just support to download Sentinel-5 product.
Please read User'guide if you want to know about the details of Sentinel-5 data. 

### Install

To install the pachage using commands as follow

```bash
   git clone https://github.com/bugsuse/pytropomi.git
   cd pytropomi
   python setup.py install
```

### Usage

The package now support to download the multi-type product, including Level1B and Level2 product of NO2, O3, SO2 and so on, data of assigned date, and you can give a longitude and latitude or a area's polygon which consisting of series longitude and latitude coordinates to filter the product     

* filter results by longitude and latitude coordinate pairs

```python
    from datetime import datetime
    from pytropomi.downs5p import downs5p
    
    beginPosition = datetime(2019, 7, 7, 0)
    endPosition = datetime(2019, 7, 7, 23)
    
    pro = 'L2_NO2___'

    longitude = 120
    latitude = 30

    downs5p(producttype=pro, longitude=longitude, latitude=latitude, processingmode='Near real time',
            beginPosition=beginPosition, endPosition=endPosition)
```

* filter results given the polygon and/or the intersection area of two polygon (polygon and area params) 
```python
   from shapely.geometry import Polygon
   
   polygon = Polygon([(100, 20), (105, 25), (110, 30), (115, 35), (120, 30), (125, 25), (130, 20), (120,
   area = 20
    
   pro = 'L2_O3____'

   downs5p(producttype=pro, polygon=polygon, area=area, processingmode='Near real time', 
           beginPosition=beginPosition, endPosition=endPosition)
```

Please check the scripts inside the examples directory to get the usage about the package.


