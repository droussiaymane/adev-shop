from django import forms
from django_countries.fields import CountryField
class add_to_cart(forms.Form):
    size=forms.CharField(max_length=10)
    color=forms.CharField(max_length=100)
    quantity=forms.IntegerField()

class billing_adress(forms.Form):
    first_name=forms.CharField(max_length=100,)
    last_name=forms.CharField(max_length=100,)
    adress1=forms.CharField(max_length=200,)
    adress2=forms.CharField(max_length=200,)
    city=forms.CharField(max_length=50,)
    zip=forms.IntegerField()
    phone=forms.IntegerField()
    country=CountryField(blank_label='(select country)').formfield()
    