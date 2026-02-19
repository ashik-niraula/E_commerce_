from django import forms
from e_auth.models import Address , Customer , Profile , Vendor
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User



class UserRegistration(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['email','username','first_name', 'last_name' ,'password1','password2']#,'is_costomer','is_vendor','contact']

class VendorDetailForm(forms.ModelForm)     :
    class Meta:
        model = Vendor
        fields = ['shop_name','pan'] 

class AddressForm(forms.ModelForm)      :
    class Meta:
        model = Address
        exclude = ['profile']

