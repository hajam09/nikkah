from django_countries import countries

from core.choices import (
    EatingHabit,
    EducationLevel,
    EmploymentStatus,
    FamilyStatus,
    FamilyType,
    FamilyValue,
    Industry,
    Language,
    MaritalStatus,
    Madhab,
    PhysicalStatus,
    PrayerFrequency,
    QuranReading,
    SmokingHabit,
)

USER_PROFILE_RELATIONS = (
    'matrimonialProfile',
    'religiousProfile',
    'educationProfile',
    'careerProfile',
    'locationProfile',
    'familyProfile',
    'waliProfile',
    'partnerPreference',
)

MATRIMONIAL_PROFILE_RELATIONS = (
    'user__religiousProfile',
    'user__educationProfile',
    'user__careerProfile',
    'user__locationProfile',
    'user__familyProfile',
    'user__waliProfile',
    'user__partnerPreference',
)

MATRIMONIAL_PROFILE_FIELD_FILTERS = {
    # MatrimonialProfile
    'createdBy': 'createdBy__in',
    'maritalStatus': 'maritalStatus__in',
    'physicalStatus': 'physicalStatus__in',
    'weight': 'weight__in',
    'eatingHabit': 'eatingHabit__in',
    'smokingHabit': 'smokingHabit__in',
    'nationality': 'nationality__in',
    'minHeight': 'height__gte',
    'maxHeight': 'height__lte',

    # ReligiousProfile
    'madhab': 'user__religiousProfile__madhab__in',
    'prayerFrequency': 'user__religiousProfile__prayerFrequency__in',
    'quranReading': 'user__religiousProfile__quranReading__in',
    'hijabStatus': 'user__religiousProfile__hijabStatus__in',

    # CareerProfile
    'industry': 'user__careerProfile__industry__in',
    'employmentStatus': 'user__careerProfile__employmentStatus__in',

    # EducationProfile
    'educationLevel': 'user__educationProfile__educationLevel__in',

    # LocationProfile
    'residency': 'user__locationProfile__residency__in',
    'city': 'user__locationProfile__city__icontains',

    # FamilyProfile
    'familyStatus': 'user__familyProfile__familyStatus__in',
    'familyType': 'user__familyProfile__familyType__in',
    'familyValue': 'user__familyProfile__familyValue__in',
}

MATRIMONIAL_PROFILE_BOOLEAN_FIELD_FILTERS = {
    'observesFasting': 'user__religiousProfile__observesFasting',
    'halalLifestyle': 'user__religiousProfile__halalLifestyle',
    'willingToRelocate': 'user__locationProfile__willingToRelocate',
}

PROFILE_SECTIONS = [
    ('Matrimonial profile', 'core:settings-matrimonial', 'matrimonialProfile'),
    ('Religious profile', 'core:settings-religious', 'religiousProfile'),
    ('Education profile', 'core:settings-education', 'educationProfile'),
    ('Career profile', 'core:settings-career', 'careerProfile'),
    ('Location profile', 'core:settings-location', 'locationProfile'),
    ('Family profile', 'core:settings-family', 'familyProfile'),
    ('Wali profile', 'core:settings-wali', 'waliProfile'),
    ('Partner preferences', 'core:settings-preferences', 'partnerPreference'),
]

SETTINGS_PANEL = [
    ('Personal profile', 'core:settings-personal'),
    ('Change password', 'core:settings-password'),
    ('Matrimonial profile', 'core:settings-matrimonial'),
    ('Religious profile', 'core:settings-religious'),
    ('Education profile', 'core:settings-education'),
    ('Career profile', 'core:settings-career'),
    ('Location profile', 'core:settings-location'),
    ('Family profile', 'core:settings-family'),
    ('Wali profile', 'core:settings-wali'),
    ('Partner preferences', 'core:settings-preferences'),
]

COUNTRY_CHOICES = tuple((name, name) for _, name in countries)
NIKKAH_AGE_CHOICES = tuple((str(age), str(age)) for age in range(18, 70))
ANY_PREFERENCE = '__ANY__'
FIVE_OR_MORE_CHILDREN = '5PLUS'
CHILDREN_CHOICES = (
    ('0', 'No children'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    (FIVE_OR_MORE_CHILDREN, '5 or more'),
)

PARTNER_PREFERENCES_DETAIL_PANEL = {
    'maritalStatus': MaritalStatus.choices,
    'children': CHILDREN_CHOICES,
    'physicalStatus': PhysicalStatus.choices,
    'eatingHabit': EatingHabit.choices,
    'smokingHabit': SmokingHabit.choices,
    'languages': Language.choices,
    'educationLevel': EducationLevel.choices,
    'employmentStatus': EmploymentStatus.choices,
    'industry': Industry.choices,
    'madhab': Madhab.choices,
    'prayerFrequency': PrayerFrequency.choices,
    'quranReading': QuranReading.choices,
    'observesFasting': (('YES', 'Yes'), ('NO', 'No')),
    'familyStatus': FamilyStatus.choices,
    'familyType': FamilyType.choices,
    'familyValue': FamilyValue.choices,
}


class MatchesPanel:
    def __init__(self, match, icon, name, description, heading):
        self.match = match
        self.icon = icon
        self.name = name
        self.description = description
        self.heading = heading


# 1. Based on activity
MATCHES_PANEL_BASED_ON_ACTIVITY = [
    MatchesPanel('shortlisted-by-you', 'bi bi-star-fill', 'Shortlisted By You',
                 'Matches you have shortlisted', 'Matches shortlisted by you'),
    MatchesPanel('viewed-you', 'bi bi-eye', 'Viewed You',
                 'Matches who have viewed your profile', 'Matches who have viewed your profile'),
    MatchesPanel('shortlisted-you', 'bi bi-person-plus', 'Shortlisted You',
                 'Matches who have shortlisted your profile', 'Matches who shortlisted you'),
    MatchesPanel('viewed-by-you', 'bi bi-person-check', 'Viewed By You',
                 'Matches you have viewed', 'Profiles you have viewed'),
]

# 2. Recently joined & nearby matches
MATCHES_PANEL_RECENTLY_JOINED_AND_NEARBY = [
    MatchesPanel('newly-joined', 'bi bi-person-plus', 'Newly Joined',
                 'Matches who joined within the last 30 days', 'Newly joined matches'),
    MatchesPanel('nearby', 'bi bi-geo-alt', 'Nearby Matches',
                 'Matches near your location', 'Nearby matches'),
]

# 3. Based on profile details
MATCHES_PANEL_BASED_ON_PROFILE_DETAILS = [
    MatchesPanel('with-photos', 'bi bi-person-badge', 'Matches with photos',
                 'Matches that have added photos', 'Matches with photos'),
    MatchesPanel('verified', 'bi bi-patch-check', 'Verified members',
                 'Profiles verified by the Nikkah team', 'Verified members'),
    MatchesPanel('recently-active', 'bi bi-clock-history', 'Recently active',
                 'Members active within the last 30 days', 'Recently active members'),
    MatchesPanel('created-by-family', 'bi bi-person-hearts', 'Created by family',
                 'Profiles created by a parent or relative', 'Profiles created by family'),
]

# 4. Personal & marital status
MATCHES_PANEL_PERSONAL_AND_MARITAL_STATUS = [
    MatchesPanel('single', 'bi bi-person', 'Single',
                 'Matches who have never married', 'Single matches'),
    MatchesPanel('divorced', 'bi bi-person-dash', 'Divorced',
                 'Matches who are divorced', 'Divorced matches'),
    MatchesPanel('widowed', 'bi bi-person-heart', 'Widowed',
                 'Matches who are widowed', 'Widowed matches'),
    MatchesPanel('no-children', 'bi bi-person', 'Without children',
                 'Matches who do not have children', 'Matches without children'),
    MatchesPanel('with-children', 'bi bi-people', 'With children',
                 'Matches who have children', 'Matches with children'),
    MatchesPanel('age-18-25', 'bi bi-cake2', 'Aged 18-25',
                 'Matches within this age range', 'Matches aged 18-25'),
    MatchesPanel('age-26-35', 'bi bi-cake2', 'Aged 26-35',
                 'Matches within this age range', 'Matches aged 26-35'),
    MatchesPanel('age-36-plus', 'bi bi-cake2', 'Aged 36 plus',
                 'Matches aged 36 and over', 'Matches aged 36 plus'),
]

# 5. Members who are looking for someone like you
MATCHES_PANEL_LOOKING_FOR_YOU = [
    MatchesPanel('mutual', 'bi bi-hearts', 'Mutual Matches',
                 'Matches whose profile match your preferences and vice versa', 'Mutual matches'),
    MatchesPanel('looking-for-you', 'bi bi-globe2', 'Looking For You',
                 'Matches whose preferences match your profile', 'Members looking for someone like you'),
]

# 6. Religious & lifestyle preferences
MATCHES_PANEL_RELIGIOUS_AND_LIFESTYLE_PREFERENCES = [
    MatchesPanel('madhab', 'bi bi-book', 'By madhab',
                 'Matches with your preferred Islamic school', 'Matches by madhab'),
    MatchesPanel('prayer', 'bi bi-sun', 'Prayer practice',
                 'Matches with similar prayer habits', 'Matches by prayer practice'),
    MatchesPanel('eating', 'bi bi-egg-fried', 'Eating preference',
                 'Matches with compatible eating habits', 'Matches by eating preference'),
    MatchesPanel('non-smoker', 'bi bi-ban', 'Non-smokers',
                 'Matches who do not smoke', 'Non-smoking matches'),
]

# 7. Family & relocation
MATCHES_PANEL_FAMILY_AND_RELOCATION = [
    MatchesPanel('family-values', 'bi bi-house-heart', 'Family values',
                 'Matches with compatible family values', 'Matches with compatible family values'),
    MatchesPanel('family-type', 'bi bi-houses', 'Family type',
                 'Matches by nuclear or joint family preference', 'Matches by family type'),
    MatchesPanel('relocate', 'bi bi-truck', 'Willing to relocate',
                 'Matches open to relocating', 'Matches willing to relocate'),
]

# 8. Matches based on preferences
MATCHES_PANEL_BASED_ON_PREFERENCES = [
    MatchesPanel('education', 'bi bi-mortarboard', 'Education preference',
                 'Matches based on your preferred education', 'Education preference'),
    MatchesPanel('professional', 'bi bi-briefcase', 'Professional preference',
                 'Matches based on your preferred profession', 'Professional preference'),
    MatchesPanel('location', 'bi bi-geo-alt', 'City/location preference',
                 'Matches based on your preferred location', 'City/location preference'),
]

# All sections combined
MATCHES_PANEL_SECTIONS = [
    {
        'title': 'Based on activity',
        'panels': MATCHES_PANEL_BASED_ON_ACTIVITY,
    },
    {
        'title': 'Recently joined & nearby matches',
        'panels': MATCHES_PANEL_RECENTLY_JOINED_AND_NEARBY,
    },
    {
        'title': 'Based on profile details',
        'panels': MATCHES_PANEL_BASED_ON_PROFILE_DETAILS,
    },
    {
        'title': 'Personal & marital status',
        'panels': MATCHES_PANEL_PERSONAL_AND_MARITAL_STATUS,
    },
    {
        'title': 'Members who are looking for someone like you',
        'panels': MATCHES_PANEL_LOOKING_FOR_YOU,
    },
    {
        'title': 'Religious & lifestyle preferences',
        'panels': MATCHES_PANEL_RELIGIOUS_AND_LIFESTYLE_PREFERENCES,
    },
    {
        'title': 'Family & relocation',
        'panels': MATCHES_PANEL_FAMILY_AND_RELOCATION,
    },
    {
        'title': 'Matches based on preferences',
        'panels': MATCHES_PANEL_BASED_ON_PREFERENCES,
    },
]
