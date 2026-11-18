import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm

from core.models import MatrimonialProfile, User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'username',
            'autofocus': True,
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'current-password',
            'placeholder': 'Password',
        })


class PersonalProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class MatrimonialProfileForm(forms.ModelForm):
    dateOfBirth = forms.DateField(
        label='Date of birth',
        input_formats=['%Y-%m'],
        widget=forms.DateInput(format='%Y-%m', attrs={'type': 'month'}),
        required=True,
    )
    height = forms.CharField(
        label='Height',
        help_text='Enter centimeters, meters, or feet and inches (for example: 170 cm, 1.70 m, or 5 ft 7 in).',
        widget=forms.TextInput(attrs={
            'placeholder': '170 cm, 1.70 m, or 5 ft 7 in',
            'inputmode': 'decimal',
        }),
    )

    class Meta:
        model = MatrimonialProfile
        fields = (
            'gender',
            'dateOfBirth',
            'height',
            'maritalStatus',
            'numberOfChildren',
            'nationality',
            'ethnicity',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('gender', 'dateOfBirth', 'height', 'maritalStatus'):
            self.fields[field_name].required = True
        for field in self.fields.values():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css_class

    def clean_height(self):
        value = self.cleaned_data['height'].strip().lower()
        centimeters_match = re.fullmatch(r'(\d+(?:\.\d+)?)\s*(?:cm|centimeters?)?', value)
        meters_match = re.fullmatch(r'(\d+(?:\.\d+)?)\s*(?:m|meters?)', value)
        feet_inches_match = re.fullmatch(
            r"(\d+)\s*(?:ft|feet|')\s*(?:(\d+(?:\.\d+)?)\s*(?:in|inches?|\"))?",
            value,
        )

        try:
            if centimeters_match:
                centimeters = Decimal(centimeters_match.group(1))
            elif meters_match:
                centimeters = Decimal(meters_match.group(1)) * 100
            elif feet_inches_match:
                feet = Decimal(feet_inches_match.group(1))
                inches = Decimal(feet_inches_match.group(2) or 0)
                if inches >= 12:
                    raise forms.ValidationError('Enter fewer than 12 inches with the feet value.')
                centimeters = (feet * 12 + inches) * Decimal('2.54')
            else:
                raise forms.ValidationError(
                    'Enter a height in centimeters, meters, or feet and inches.'
                )
        except InvalidOperation as error:
            raise forms.ValidationError('Enter a valid height.') from error

        centimeters = centimeters.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        if centimeters < 1 or centimeters > 300:
            raise forms.ValidationError('Enter a height between 1 and 300 centimeters.')
        return int(centimeters)


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['autocomplete'] = (
                'current-password' if field_name == 'old_password' else 'new-password'
            )
