from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Shop


class ShopForm(ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'
        # exclude = ['user']
