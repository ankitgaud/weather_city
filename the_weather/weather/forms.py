from django import forms

from .models import City

from django.contrib.auth import (
    authenticate,
    get_user_model

)

User = get_user_model()

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'}),
        } #updates the input class to have the correct Bulma class and placeholder




class UserLoginForm(forms.Form):
    username = forms.CharField(
    	max_length=40,
    	widget=forms.TextInput(attrs={
    		'class': 'User_name', 
    		'placeholder': 'Username'
    		}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    	'class': 'Password',
    	'placeholder': 'Password',
    	}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)




class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={
            'class': 'User_name', 
            'placeholder': 'Username'
            }))
    email = forms.EmailField(label='Email address',
        widget=forms.TextInput(attrs={
        'class': 'email', 
        'placeholder': 'Enter email'
            })
        )
    email2 = forms.EmailField(label='Confirm Email',
        widget=forms.TextInput(attrs={
        'class': 'email2', 
        'placeholder': 'Confirm email'
            })
        )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'Password',
        'placeholder': 'Password',

        }))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        user_exist = User.objects.filter(username=username)
        if username == user_exist:
            raise forms.ValidationError("Username already exists!")
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)

