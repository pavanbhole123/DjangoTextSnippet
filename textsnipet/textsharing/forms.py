from django import forms

class TextForm(forms.Form):
    text_msg = forms.CharField(widget=forms.Textarea)
    enc = forms.BooleanField(required=False)
    enc_key = forms.CharField(max_length=32, required= False)

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput()) 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

class EncKeyForm(forms.Form):
    enc_key = forms.CharField(max_length=32, required= False)