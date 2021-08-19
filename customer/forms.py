from django import forms
from django.utils.translation import gettext_lazy as _
from core.validators import phone_validator
from core.models import User
from .models import *


class CustomerRegisterForm(forms.Form):
    phone = forms.CharField(
        max_length=13,
        help_text=_('Enter as the example : +989112223344'),
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                'placeholder': _('phone number')
            }
        ),
        error_messages={
            'required': _('This field is required'),
            'invalid': _('Invalid Input!'),
        },
    )
    email = forms.EmailField(
        help_text=_('Customer Email'),
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('Email')
            }
        ),
        error_messages={
            'required': _('This field is required'),
            'invalid': _('Invalid Input!'),
        },
    )
    first_name = forms.CharField(
        help_text=_('Customer Firstname'),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('First Name')
            }
        ),
        error_messages={
            'required': _('This field is required'),
            'invalid': _('Invalid Input!'),
        },
    )
    last_name = forms.CharField(
        help_text=_('Customer Lastname'),
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Last Name')
            }
        ),
        error_messages={
            'required': _('This field is required'),
            'invalid': _('Invalid Input!'),
        },
    )
    password_1 = forms.CharField(
        help_text=_('password'),
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password'),
            }
        ),
        error_messages={
            'required': _('This field is required'),
            'invalid': _('Invalid Input!'),
        },
    )
    password_2 = forms.CharField(
        help_text=_('Confirm password'),
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Confirm Password')
            }
        ),
        error_messages={
            'required': _('This field is required'),
            'invalid': _('Invalid Input!'),
        },
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('User with this phone number already exists!'))
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('User with this email already exists!'))
        return email

    def clean_password_2(self):
        password_1 = self.cleaned_data['password_1']
        password_2 = self.cleaned_data['password_2']
        if password_1 != password_2:
            raise forms.ValidationError(_('passwords are not match'))
        elif len(password_2) < 8:
            raise forms.ValidationError(_('password too short (At least 8 characters)'))
        elif not any(i.isalpha() for i in password_2):
            raise forms.ValidationError(_('The password must contain letters'))
        elif not any(i.isupper() for i in password_2):
            raise forms.ValidationError(_('The password must contain at least one capital letter'))
        return password_2


class CustomerLoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        help_text=_('Enter your phone number as the example : (+989112223344) or Enter your Email'),
        widget=forms.TextInput(
            attrs={
                'placeholder': _('PhoneNumber or Email')
            }
        ),
        error_messages={
            'required': _('This field is required'),
            'invalid': _('Invalid Input!'),
        },
    )
    password = forms.CharField(
        help_text=_('password'),
        max_length=30,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Password')
            }
        ),
        error_messages={
            'required': _('This field is required'),
            'invalid': _('Invalid Input!'),
        },
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and self.instance.email != email:
            raise forms.ValidationError(_('User with this email already exists!'))
        return email


class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['image']


class AddressFormModel(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['state', 'city', 'postal_code', 'detail', 'lat', 'lng']
