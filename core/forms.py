import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm
from django_countries import countries

from core.models import (
    CareerProfile,
    Education,
    MatrimonialProfile,
    ProfileLocation,
    ReligiousProfile,
    User,
)


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


class ReligiousProfileForm(forms.ModelForm):
    halalLifestyle = forms.TypedChoiceField(
        choices=((True, 'Yes'), (False, 'No')),
        coerce=lambda value: value == 'True',
        label='Halal lifestyle',
        widget=forms.Select,
    )

    class Meta:
        model = ReligiousProfile
        fields = (
            'madhab',
            'prayerFrequency',
            'quranReading',
            'observesFasting',
            'wearsHijab',
            'wearsNiqab',
            'halalLifestyle',
            'religiousPracticeDescription',
        )
        widgets = {
            'religiousPracticeDescription': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.Select, forms.NullBooleanSelect)):
                css_class = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            else:
                css_class = 'form-control'
            field.widget.attrs['class'] = css_class
            if not isinstance(field.widget, (forms.CheckboxInput, forms.Select, forms.NullBooleanSelect)):
                field.widget.attrs['placeholder'] = field.label


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('qualification', 'institution', 'fieldOfStudy', 'graduationYear')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css_class
            field.widget.attrs['placeholder'] = field.label


class CareerProfileForm(forms.ModelForm):
    class Meta:
        model = CareerProfile
        fields = ('employmentStatus', 'occupation', 'industry')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css_class
            field.widget.attrs['placeholder'] = field.label


class ProfileLocationForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=(('', 'Select a country'),) + tuple((name, name) for _, name in countries),
        label='Country',
    )
    willingToRelocate = forms.TypedChoiceField(
        choices=((True, 'Yes'), (False, 'No')),
        coerce=lambda value: value == 'True',
        label='Willing to relocate',
        widget=forms.Select,
    )
    preferredCountries = forms.MultipleChoiceField(
        choices=tuple((name, name) for _, name in countries),
        required=False,
        label='Preferred countries',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'placeholder': 'Select preferred countries',
            'data-country-tags': 'true',
        }),
    )

    class Meta:
        model = ProfileLocation
        fields = ('town', 'city', 'country', 'willingToRelocate', 'preferredCountries')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            if hasattr(self.data, 'getlist'):
                submitted_countries = self.data.getlist('preferredCountries')
            else:
                submitted_countries = self.data.get('preferredCountries', [])
                if isinstance(submitted_countries, str):
                    submitted_countries = [submitted_countries]
        else:
            submitted_countries = []
        existing_countries = self.instance.preferredCountries if self.instance.pk else []
        country_names = {name for _, name in countries}
        legacy_countries = [
            value for value in existing_countries
            if value not in country_names
        ]
        if self.instance.pk and self.instance.country and self.instance.country not in country_names:
            self.fields['country'].choices += ((self.instance.country, self.instance.country),)
        if legacy_countries:
            self.fields['preferredCountries'].choices += tuple(
                (value, value) for value in legacy_countries
            )
        self.fields['preferredCountries'].widget.choices = self.fields['preferredCountries'].choices

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-select' if isinstance(
                field.widget, forms.Select
            ) else 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean_preferredCountries(self):
        countries = self.cleaned_data['preferredCountries']
        if not self.cleaned_data.get('willingToRelocate'):
            return []
        if len(countries) > 50:
            raise forms.ValidationError('Select no more than 50 preferred countries.')
        return countries


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['autocomplete'] = (
                'current-password' if field_name == 'old_password' else 'new-password'
            )
