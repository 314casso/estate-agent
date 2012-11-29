from django import forms
from estatebase.models import Origin
from maxim_base.models import Source

class SourceOriginForm(forms.ModelForm):
    source = forms.ModelChoiceField(queryset=Source.objects.all())
    def __init__(self, *args, **kwargs):
        super(SourceOriginForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['source'].initial = self.instance.source_id             
    class Meta:
        model = Origin
        exclude = ['source_id']        