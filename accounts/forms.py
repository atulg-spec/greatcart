from django import forms
from .models import CustomUser

class PhoneNumberForm(forms.Form):
    phone_number = forms.IntegerField(label='Phone Number')

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'address_line_1', 'address_line_2', 'city', 'state', 'zip_code', 'country')