from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(label='username', max_length=20)
    password = forms.CharField(label='password', max_length=50)
    confirm_password = forms.CharField(label='confirm_password', max_length=50)


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=20)
    password = forms.CharField(label='password', max_length=50)
