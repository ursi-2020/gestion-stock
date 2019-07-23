from django.forms import ModelForm
from .models import Article, Data

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['nom', 'stock']


class DataForm(ModelForm):
    class Meta:
        model = Data
        fields = ['text', 'date']