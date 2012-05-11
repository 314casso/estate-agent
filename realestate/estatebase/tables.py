import django_tables2 as tables 
from django_tables2.utils import A

class EstateTable(tables.Table):    
    street = tables.Column(accessor='street.name')
    pk = tables.LinkColumn('estate_update', args=[A('pk')], attrs={'class':'ajax-dialog'})
    class Meta:
        attrs = {'class': 'paleblue'}

class ClientTable(tables.Table):    
    name = tables.Column(accessor='name')
    pk = tables.LinkColumn('estate_update', args=[A('pk')], attrs={'class':'ajax-dialog'})
    class Meta:
        attrs = {'class': 'paleblue'}        
