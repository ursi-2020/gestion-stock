from django.forms import ModelForm
from django import forms
from .models import Article

valid_date_time=["%d/%m/%Y-%H:%M:%S"]
recurrence_choice= [
    ('none', 'Aucun'),
    ('minute', 'Minute'),
    ('hour', 'Heure'),
    ('day', 'Jour'),
    ('week', 'Semaine'),
    ('month', 'Mois'),
    ('year', 'An'),
    ]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['nom', 'stock']

class ScheduleForm(forms.Form):
    host = forms.CharField(label='Host', max_length=150, widget=forms.TextInput())
    url = forms.CharField(label='Url', max_length=150, widget=forms.TextInput())
    time = forms.DateTimeField(label='Time', input_formats=valid_date_time,
              widget=forms.DateTimeInput(attrs={'placeholder': '%d/%m/%Y-%H:%M:%S'}))
    recurrence = forms.CharField(label='Recurrence', widget=forms.Select(choices=recurrence_choice))
    data = forms.CharField(label='Data', max_length=150, required=False, widget=forms.TextInput())
    name = forms.CharField(label='Name', max_length=150, widget=forms.TextInput())
