import django_tables2 as tables 
from django_tables2.utils import A

class EstateTable(tables.Table):    
    street = tables.Column(accessor='street.name')
    pk = tables.LinkColumn('estate_update', args=[A('pk')], attrs={'class':'ajax-dialog'})
    class Meta:
        attrs = {'class': 'paleblue'}


def getLinkTemplate(url_name, value):
        return '<a href="{% url ' + url_name + ' record.pk %}?{{ next_url }}">' + value +  '</a>'

class ClientTable(tables.Table):
    pk = tables.Column(verbose_name='Id')
    name = tables.TemplateColumn(getLinkTemplate('client_update','{{record.name }}'))
    client_type = tables.Column()     
    origin = tables.Column()
    address = tables.Column()
    #TODO: Move to template file  
    contacts = tables.TemplateColumn('{% for item in record.contact_set.all %}<span class="contact-inline"><label>{{ item.contact_type }}:</label> {{ item.contact }}</span>{% endfor %}', orderable=False)
    remove = tables.TemplateColumn(getLinkTemplate('client_delete','Delete'), orderable=False)
            
    class Meta:
        attrs = {'class': 'paleblue'}       
        order_by  = ('pk',)
         
