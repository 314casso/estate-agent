import django_tables2 as tables 
from django_tables2.utils import A

class EstateTable(tables.Table):
    #id = tables.Column(accessor='id')
    street = tables.Column(accessor='street.name')
    pk = tables.LinkColumn('estate_update', args=[A('pk')], attrs={'class':'ajax-dialog'})
    class Meta:
        attrs = {'class': 'paleblue'}
        