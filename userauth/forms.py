from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .validator import ValidatePassword
from .models import CustomUser


class UserSignUp(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'nickname', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        validator = ValidatePassword()
        validator.validate(password)
        return password
    
    def save(self, commit=True):
        user = super(UserSignUp, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.is_active = False
            user.save()
        return user    
        

class passwordChangeForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
        (
            attrs={'autocomplete': 'new-password'}
        ), 
            label="New Password"
    )
    confirmPassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password'}
        ), label="New Confirm Password"
    )
    class Meta:
        model = CustomUser
        fields = []

class LoginForm(AuthenticationForm):
    pass