from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm
from django.utils import timezone

from core.choices import (
    CreatedBy,
    EatingHabit,
    EducationLevel,
    EmploymentStatus,
    FamilyType,
    FamilyValue,
    FamilyStatus,
    Gender,
    Height,
    HijabStatus,
    Industry,
    Language,
    MaritalStatus,
    Madhab,
    PhysicalStatus,
    PrayerFrequency,
    QuranReading,
    SmokingHabit,
    Weight,
)
from core.constants import COUNTRY_CHOICES, NIKKAH_AGE_CHOICES
from core.models import (
    User,
    MatrimonialProfile,
    ReligiousProfile,
    EducationProfile,
    CareerProfile,
    LocationProfile,
    FamilyProfile,
    WaliProfile,
    PartnerPreference,
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


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['autocomplete'] = (
                'current-password' if field_name == 'old_password' else 'new-password'
            )


class NikkahForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, (forms.Select, forms.SelectMultiple)) else 'form-control'
            field.widget.attrs['class'] = css


class MatrimonialProfileForm(NikkahForm):
    languages = forms.MultipleChoiceField(
        choices=Language.choices,
        required=False,
        widget=forms.SelectMultiple,
    )
    dateOfBirth = forms.DateField(
        label='Date of birth',
        input_formats=['%Y-%m'],
        widget=forms.DateInput(format='%Y-%m', attrs={'type': 'month', 'max': timezone.localdate().strftime('%Y-%m')}),
        required=True,
    )
    nationality = forms.ChoiceField(
        choices=(('', '---------'),) + COUNTRY_CHOICES,
    )

    class Meta:
        model = MatrimonialProfile
        exclude = ('user',)
        widgets = {
            'numberOfChildren': forms.NumberInput(attrs={
                'min': 0,
                'max': 10,
            }),
            'aboutMe': forms.Textarea(attrs={
                'rows': 5,
                'maxlength': 1000,
                'placeholder': 'Tell us something about yourself...'
            }),
        }
        labels = {
            'createdBy': 'Profile created by',
            'gender': 'Gender',
            'dateOfBirth': 'Date of birth',
            'height': 'Height',
            'weight': 'Weight',
            'maritalStatus': 'Marital status',
            'physicalStatus': 'Physical status',
            'languages': 'Languages spoken',
            'eatingHabit': 'Eating habit',
            'smokingHabit': 'Smoking habit',
            'numberOfChildren': 'Number of children',
            'nationality': 'Nationality',
            'aboutMe': 'About me',
        }


class ReligiousProfileForm(NikkahForm):
    class Meta:
        model = ReligiousProfile
        exclude = ('user',)
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 5,
                'maxlength': 1000,
                'placeholder': 'Tell us something about your religious beliefs and practices...'
            }),
        }
        labels = {
            'madhab': 'Madhab',
            'prayerFrequency': 'Prayer frequency',
            'quranReading': 'Quran reading',
            'hijabStatus': 'Hijab / niqab',
            'observesFasting': 'Observes fasting',
            'halalLifestyle': 'Halal lifestyle',
            'description': 'Description',
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gender = request.user.matrimonialProfile.gender if hasattr(request.user, 'matrimonialProfile') else None
        if self.gender == Gender.MALE:
            self.fields.pop('hijabStatus', None)
            self.instance.hijabStatus = None


class EducationProfileForm(NikkahForm):
    class Meta:
        model = EducationProfile
        exclude = ('user',)
        labels = {
            'qualification': 'Qualification',
            'institution': 'Institution',
            'fieldOfStudy': 'Field of Study',
            'graduationYear': 'Graduation year',
        }


class CareerProfileForm(NikkahForm):
    class Meta:
        model = CareerProfile
        exclude = ('user',)
        labels = {
            'employmentStatus': 'Employment Status',
            'occupation': 'Occupation',
            'industry': 'Industry',
        }


class LocationProfileForm(NikkahForm):
    residency = forms.ChoiceField(
        choices=(('', '---------'),) + COUNTRY_CHOICES,
    )
    citizenShip = forms.MultipleChoiceField(
        choices=COUNTRY_CHOICES,
        required=False,
        widget=forms.SelectMultiple,
    )
    preferredCountries = forms.MultipleChoiceField(
        choices=COUNTRY_CHOICES,
        required=False,
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = LocationProfile
        exclude = ('user',)
        labels = {
            'town': 'Town',
            'city': 'City',
            'nativePlace': 'Native place',
            'residency': 'Country of residence',
            'citizenShip': 'Citizenship',
            'willingToRelocate': 'Willing to relocate',
            'preferredCountries': 'Preferred countries',
        }

    def clean_preferredCountries(self):
        if self.cleaned_data.get('willingToRelocate') is False:
            return []
        return self.cleaned_data['preferredCountries']


class FamilyProfileForm(NikkahForm):
    class Meta:
        model = FamilyProfile
        exclude = ('user',)
        widgets = {
            'aboutMyFamily': forms.Textarea(attrs={
                'rows': 5,
                'maxlength': 1000,
                'placeholder': 'Tell us something about your family...'
            }),
        }
        labels = {
            'fatherOccupation': 'Father\'s occupation',
            'motherOccupation': 'Mother\'s occupation',
            'numberOfSiblings': 'Number of siblings',
            'familyStatus': 'Family status',
            'familyType': 'Family type',
            'familyValue': 'Family values',
            'aboutMyFamily': 'About my family',
        }


class WaliProfileForm(NikkahForm):
    class Meta:
        model = WaliProfile
        exclude = ('user',)
        labels = {
            'fullName': 'Wali name',
            'relationship': 'Relationship with wali',
            'email': 'Wali email',
            'phone': 'Wali phone number',
            'consentToContact': 'Consent to contact',
            'isVerified': 'Wali verified',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['isVerified'].disabled = True


class PartnerPreferenceForm(NikkahForm):
    ANY_CHOICE = (('__ANY__', 'Any'),)

    madhab = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(Madhab.choices))
    prayerFrequency = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(PrayerFrequency.choices))
    eatingHabit = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(EatingHabit.choices))
    class Meta:
        model = PartnerPreference
        exclude = ('user',)
        labels = {
            'minAge': 'Minimum age',
            'maxAge': 'Maximum age',
            'madhab': 'Madhab',
            'prayerFrequency': 'Prayer frequency',
            'eatingHabit': 'Eating habit',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        labels = self.Meta.labels
        for name, field in self.fields.items():
            field.required = False

            if name in labels:
                field.label = labels[name]


class ProfileSearchForm(forms.Form):
    ANY_CHOICE = (('__ANY__', 'Any'),)
    AGE_CHOICES = (('', 'Any'),) + NIKKAH_AGE_CHOICES
    HEIGHT_CHOICES = (('', 'Any'),) + tuple(Height.choices)
    CREATED_CHOICES = (
        ('', 'Any time'),
        ('1', 'Today'),
        ('3', 'Last 3 days'),
        ('7', 'One week'),
        ('30', 'One month'),
    )
    CHILDREN_CHOICES = (
        ('0', 'No children'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5PLUS', '5 or more'),
    )
    YES_NO_CHOICES = (
        ('__ANY__', 'Any'),
        ('YES', 'Yes'),
        ('NO', 'No'),
    )

    minAge = forms.ChoiceField(choices=AGE_CHOICES)
    maxAge = forms.ChoiceField(choices=AGE_CHOICES)
    minHeight = forms.ChoiceField(choices=HEIGHT_CHOICES)
    maxHeight = forms.ChoiceField(choices=HEIGHT_CHOICES)

    createdBy = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(CreatedBy.choices))
    maritalStatus = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(MaritalStatus.choices))
    children = forms.MultipleChoiceField(choices=ANY_CHOICE + CHILDREN_CHOICES)
    language = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(Language.choices))
    physicalStatus = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(PhysicalStatus.choices))
    weight = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(Weight.choices))
    nationality = forms.MultipleChoiceField(choices=ANY_CHOICE + COUNTRY_CHOICES)

    eatingHabit = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(EatingHabit.choices))
    smokingHabit = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(SmokingHabit.choices))
    madhab = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(Madhab.choices))
    prayerFrequency = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(PrayerFrequency.choices))
    quranReading = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(QuranReading.choices))
    hijabStatus = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(HijabStatus.choices))
    observesFasting = forms.MultipleChoiceField(choices=YES_NO_CHOICES)
    halalLifestyle = forms.MultipleChoiceField(choices=YES_NO_CHOICES)

    industry = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(Industry.choices))
    employmentStatus = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(EmploymentStatus.choices))
    educationLevel = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(EducationLevel.choices))

    residency = forms.MultipleChoiceField(choices=ANY_CHOICE + COUNTRY_CHOICES)
    city = forms.CharField(max_length=100)
    citizenship = forms.MultipleChoiceField(choices=ANY_CHOICE + COUNTRY_CHOICES)
    willingToRelocate = forms.MultipleChoiceField(choices=YES_NO_CHOICES)

    # Family
    familyStatus = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(FamilyStatus.choices))
    familyType = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(FamilyType.choices))
    familyValue = forms.MultipleChoiceField(choices=ANY_CHOICE + tuple(FamilyValue.choices))

    # Profile
    profileCreated = forms.ChoiceField(choices=CREATED_CHOICES)
    verified = forms.BooleanField()

    class Meta:
        labels = {
            'createdBy': 'Profile created by',
            'maritalStatus': 'Marital status',
            'children': 'Children',
            'language': 'Languages',
            'physicalStatus': 'Physical status',
            'weight': 'Weight',
            'nationality': 'Nationality',
            'eatingHabit': 'Eating habits',
            'smokingHabit': 'Smoking habits',
            'madhab': 'Madhab',
            'prayerFrequency': 'Prayer frequency',
            'quranReading': 'Quran reading',
            'hijabStatus': 'Hijab / Niqab',
            'observesFasting': 'Observes fasting',
            'halalLifestyle': 'Halal lifestyle',
            'industry': 'Industry',
            'employmentStatus': 'Employment type',
            'educationLevel': 'Education',
            'residency': 'Country of residence',
            'city': 'City / district',
            'citizenship': 'Citizenship',
            'willingToRelocate': 'Willing to relocate',
            'familyStatus': 'Family status',
            'familyType': 'Family type',
            'familyValue': 'Family values',
            'profileCreated': 'Profile created',
            'verified': 'Verified profiles only',
        }

    def __init__(self, *args, **kwargs):
        self.includeHijabStatus = kwargs.pop('includeHijabStatus', True)
        super().__init__(*args, **kwargs)

        labels = self.Meta.labels
        for name, field in self.fields.items():
            field.required = False

            if name in labels:
                field.label = labels[name]

        if not self.includeHijabStatus:
            self.fields.pop('hijabStatus', None)

        for name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):
                css = 'form-check-input'
            elif isinstance(widget, forms.Select):
                css = 'form-select'
            else:
                css = 'form-control'

            widget.attrs['class'] = css

            if isinstance(widget, forms.SelectMultiple):
                widget.attrs.update({
                    'size': min(6, len(field.choices)),
                    'data-any-multiselect': 'true',
                })

                if not self.is_bound:
                    field.initial = ['__ANY__']

    def validate_range(self, cleaned_data, minimum, maximum, error, converter=int):
        min_value = cleaned_data.get(minimum)
        max_value = cleaned_data.get(maximum)

        if min_value and max_value:
            if converter(min_value) > converter(max_value):
                self.add_error(maximum, error)

    def clean(self):
        cleaned_data = super().clean()

        # Age validation
        self.validate_range(
            cleaned_data,
            'minAge',
            'maxAge',
            'Maximum age must be greater than or equal to minimum age.',
        )

        # Height validation
        self.validate_range(
            cleaned_data,
            'minHeight',
            'maxHeight',
            'Maximum height must be greater than or equal to minimum height.',
        )

        # Handle Any selections
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.SelectMultiple):
                continue

            selected = cleaned_data.get(name, [])

            realChoices = {
                value for value, _ in field.choices
                if value != self.ANY_CHOICE[0][0]
            }

            if self.ANY_CHOICE[0][0] in selected or realChoices.issubset(selected):
                cleaned_data[name] = []

        return cleaned_data
