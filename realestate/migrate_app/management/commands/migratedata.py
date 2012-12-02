from django.core.management.base import BaseCommand, CommandError
import sys
from maxim_base.models import Source
from migrate_app.models import SourceOrigin
from estatebase.models import Origin


class Command(BaseCommand):
    args = '<function_name function_name ...>'
    help = 'Migrate date'

    def handle(self, *args, **options):
        for function_name in args:
            try:
                func = getattr(self, function_name)
                if callable(func):
                    func()
                else:
                    sys.stderr.write('%s is not callable' % function_name)
            except Exception, err:                
                raise CommandError('ERROR: %s\n' % str(err))
    def origin(self):
        imported = list(SourceOrigin.objects.using('default').values_list('source_id', flat=True))
        sources = Source.objects.using('maxim_db').exclude(pk__in=imported)
        for source in sources:
            origin = Origin.objects.using('default').get(name__exact=source.name)                        
            SourceOrigin.objects.using('default').create(source_id=source.pk, origin=origin)
        
            