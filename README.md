# pytropomi
python module to download Sentinel-5 from s5phub data center of [TROPOMI](http://www.tropomi.eu) site, and now just support download Sentinel-5 product.

### Install

To install the pachage using below command

```bash
   git clone https://github.com/bugsuse/pytropomi.git
   cd pytropomi
   python setup.py install
```

### Usage

The package now support to download the multi product type and level data of assigned date, and you can give a longitude and latitude or a area's polygon which consisting of series longitude and latitude coordinates to filter the product     

* filter results based on position coordinate (longitude and latitude params)
* filter results based on polygon and/or the intersection area of two polygon (polygon and area params) 

Please check the examples to get the package's usage

