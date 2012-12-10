from django import forms
from estatebase.models import Origin, EstateType
from maxim_base.models import Source, Users, Types
from django.contrib.auth.models import User

class SourceOriginForm(forms.ModelForm):
    source = forms.ModelChoiceField(queryset=Source.objects.all())
    def __init__(self, *args, **kwargs):
        super(SourceOriginForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['source'].initial = self.instance.source_id             
    class Meta:
        model = Origin
        exclude = ['source_id']

class UserUserForm(forms.ModelForm):
    source = forms.ModelChoiceField(queryset=Users.objects.all())
    def __init__(self, *args, **kwargs):
        super(UserUserForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['source'].initial = self.instance.source_id             
    class Meta:
        model = User
        exclude = ['source_id']
                        
class TypesEstateTypeForm(forms.ModelForm):
    source = forms.ModelChoiceField(queryset=Types.objects.all())
    def __init__(self, *args, **kwargs):
        super(TypesEstateTypeForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['source'].initial = self.instance.source_id             
    class Meta:
        model = EstateType
        exclude = ['source_id']                        