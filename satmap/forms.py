from django import forms
from .models import Layer, Map, Project

class MapForm(forms.ModelForm):
    class Meta:
        model = Map
        fields = ('title', 'description', 'location', 'zoom', 
        'project', 'layer', 'start_date', 'end_date')
        widgets = {
            'zoom': forms.NumberInput(attrs={
                'type': 'range', 'min': 0, 'max': 18}),
            'start_date': forms.DateInput(attrs={'id':'datepicker_start'}),
            'end_date': forms.DateInput(attrs={'id':'datepicker_end'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MapForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(
            user=user)
        

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'location', 'start_date', 'end_date', 'datasets')
        widgets = {
            'start_date': forms.DateInput(attrs={'id':'datepicker_start'}),
            'end_date': forms.DateInput(attrs={'id':'datepicker_end'}),
        }

class LayerForm(forms.ModelForm):
    class Meta:
        model = Layer
        fields = ('name', 'code', 'band', 'min', 'max', 'opacity', 'palette', 'units', 'description', 'is_collection')