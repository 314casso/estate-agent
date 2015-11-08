from exportdata.custom_makers.avitoxml import AvitoXML
from exportdata.xml_makers import SalesAgent

    
class GdeetotdomXML(AvitoXML):
    name = 'gdeetotdom'
    def get_sales_agent(self, estate):
        return GdeetotdomSalesAgent(estate)


class GdeetotdomSalesAgent(SalesAgent):
    def head_phone(self):
        return u'%s' % '8-988-669-3067'    