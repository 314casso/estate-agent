from django.db import models
from django.core.validators import RegexValidator
from south.modelsinspector import add_introspection_rules

class MinMaxField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 25)
        kwargs['blank'] = kwargs.get('blank', True)
        kwargs['null'] = kwargs.get('null', True)
        super(MinMaxField, self).__init__(*args, **kwargs)
        validators = []
        validators.append(RegexValidator(regex=r"^(?P<oper>\>|\<)(?P<n>\d+)$"))
        validators.append(RegexValidator(regex=r"^(?P<n1>\d+)\-(?P<n2>\d+)$"))
        validators.append(RegexValidator(regex=r"^(?P<n>\d+)$"))
        self.default_validators = validators

add_introspection_rules([], ["^estatebase\.fields\.MinMaxField"])
