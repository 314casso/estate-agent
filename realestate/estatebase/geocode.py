# -*- coding: utf-8 -*-
import requests


class GeoCode(object):
    """
    geo_code = GeoCode()
    address = u'Россия, Краснодарский край, Новороссийск, улица Чкалова, 48'
    print geo_code.get_point(address)
    """    
    api_key = u'80ac05d7-24b2-4971-b480-1a964968a2ea'
    def get_geodata(self, address):
        if not address:
            return         
        url = u'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode={address}&format=json'.format(api_key=self.api_key, address=address)
        r = requests.get(url)
        return r.json()
    def get_point(self, address):
        if not address:
            return
        try:
            geodata = self.get_geodata(address)
            response = geodata['response']
            if int(response['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found']) > 0:            
                point = response['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']                
                ll = point.split()
                if len(ll) == 2:
                    return {'longitude':ll[0] , 'latitude':ll[1]}
        except:
            return
