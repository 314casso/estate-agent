import django_tables2 as tables 

class EstateTable(tables.Table):
    id = tables.Column(accessor='id')
    street = tables.Column(accessor='street.name')
    class Meta:
        attrs = {'class': 'paleblue'}
        