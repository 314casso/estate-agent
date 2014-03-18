# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RealtyItem(Item):
    phone = Field()    
    desc = Field()
    name = Field()
    price = Field()
    price_digit = Field()
    link = Field()
    estate_type_id = Field() 
    region_id = Field()
    locality_id = Field()
    microdistrict = Field()
    street = Field()
    estate_number = Field()
    room_count = Field()
        


