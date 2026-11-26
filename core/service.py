from calendar import monthrange
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from core.choices import Gender, CreatedBy, MaritalStatus, SmokingHabit
from core.constants import (
    ANY_PREFERENCE,
    FIVE_OR_MORE_CHILDREN,
    MATRIMONIAL_PROFILE_RELATIONS,
    MATRIMONIAL_PROFILE_FIELD_FILTERS,
    MATRIMONIAL_PROFILE_BOOLEAN_FIELD_FILTERS,
    USER_PROFILE_RELATIONS,
)
from core.models import MatrimonialProfile, PartnerPreference, ReligiousProfile, ProfileView


def getGender(user):
    return MatrimonialProfile.objects.values_list('gender', flat=True).get(user=user)


def getOppositeGender(user):
    return Gender.FEMALE if getGender(user) == Gender.MALE else Gender.MALE


def getDateOfBirthFromAge(age):
    today = timezone.localdate()
    year = today.year - age
    month = today.month
    return today.replace(year=year, month=month, day=min(today.day, monthrange(year, month)[1]))


def getBaseMatches(user):
    return MatrimonialProfile.objects.filter(gender=getOppositeGender(user)).select_related(
        *MATRIMONIAL_PROFILE_RELATIONS
    ).exclude(user=user)


def getMatchesViewedUser(user):
    return getBaseMatches(user).filter(user__profilesViewed__viewed=user)


def getMatchesViewedByUser(user):
    return getBaseMatches(user).filter(user__profileViews__viewer=user)


def getMatchesJoinedRecently(user):
    last30Days = timezone.now() - timedelta(days=30)
    return getBaseMatches(user).filter(user__createdAt__gte=last30Days)


def getMatchesVerified(user):
    return getBaseMatches(user).filter(user__isVerified=True)


def getMatchesRecentlyActive(user):
    last30Days = timezone.now() - timedelta(days=30)
    return getBaseMatches(user).filter(user__last_login__gte=last30Days)


def getMatchesCreatedByParentOrRelative(user):
    return getBaseMatches(user).filter(
        createdBy__in=[
            CreatedBy.PARENTS,
            CreatedBy.SIBLING,
            CreatedBy.RELATIVE,
        ]
    )


def getMatchesSingle(user):
    return getBaseMatches(user).filter(maritalStatus=MaritalStatus.SINGLE)


def getMatchesDivorced(user):
    return getBaseMatches(user).filter(maritalStatus=MaritalStatus.DIVORCED)


def getMatchesWidowed(user):
    return getBaseMatches(user).filter(maritalStatus=MaritalStatus.WIDOWED)


def getMatchesWithoutChildren(user):
    return getBaseMatches(user).filter(children=0)


def getMatchesWithChildren(user):
    return getBaseMatches(user).filter(children__gt=0)


def getMatchesBetween18And25(user):
    return getBaseMatches(user).filter(
        dateOfBirth__lte=getDateOfBirthFromAge(18),
        dateOfBirth__gt=getDateOfBirthFromAge(26)
    )


def getMatchesBetween26And35(user):
    return getBaseMatches(user).filter(
        dateOfBirth__lte=getDateOfBirthFromAge(26),
        dateOfBirth__gt=getDateOfBirthFromAge(36)
    )


def getMatches36AndAbove(user):
    return getBaseMatches(user).filter(dateOfBirth__lte=getDateOfBirthFromAge(36))


def getMatchesByMadhab(user):
    matches = getBaseMatches(user)
    preference = PartnerPreference.objects.filter(user=user).first()

    if preference:
        madhabList = preference.madhab
    else:
        profile = ReligiousProfile.objects.filter(user=user).first()
        madhabList = [profile.madhab] if profile and profile.madhab else []

    if not madhabList or ANY_PREFERENCE in madhabList:
        return matches
    return matches.filter(user__religiousProfile__madhab__in=madhabList)


def getMatchesByPrayerFrequency(user):
    matches = getBaseMatches(user)
    preference = PartnerPreference.objects.filter(user=user).first()

    if preference:
        prayerFrequencyList = preference.prayerFrequency
    else:
        profile = ReligiousProfile.objects.filter(user=user).first()
        prayerFrequencyList = [profile.prayerFrequency] if profile and profile.prayerFrequency else []

    if not prayerFrequencyList or ANY_PREFERENCE in prayerFrequencyList:
        return matches
    return matches.filter(user__religiousProfile__prayerFrequency__in=prayerFrequencyList)


def getMatchesByEatingHabit(user):
    matches = getBaseMatches(user)
    preference = PartnerPreference.objects.filter(user=user).first()

    if preference:
        eatingHabitList = preference.eatingHabit
    else:
        profile = MatrimonialProfile.objects.filter(user=user).first()
        eatingHabitList = [profile.eatingHabit] if profile and profile.eatingHabit else []

    if not eatingHabitList or ANY_PREFERENCE in eatingHabitList:
        return matches
    return matches.filter(eatingHabit__in=eatingHabitList)


def getMatchesByEducation(user):
    matches = getBaseMatches(user)
    preference = PartnerPreference.objects.filter(user=user).first()
    educationLevelList = preference.educationLevel if preference else []
    if not educationLevelList or ANY_PREFERENCE in educationLevelList:
        return matches
    return matches.filter(user__educationProfile__educationLevel__in=educationLevelList)


def getMatchesMatchingMyPreference(user):
    matches = getBaseMatches(user)
    preference = PartnerPreference.objects.filter(user=user).first()
    if not preference:
        return matches

    if preference.minAge:
        matches = matches.filter(dateOfBirth__lte=getDateOfBirthFromAge(int(preference.minAge)))
    if preference.maxAge:
        matches = matches.filter(dateOfBirth__gt=getDateOfBirthFromAge(int(preference.maxAge) + 1))

    childFilters = Q()
    if ANY_PREFERENCE not in preference.children:
        for childCount in preference.children:
            if childCount == FIVE_OR_MORE_CHILDREN:
                childFilters |= Q(children__gte=5)
            else:
                childFilters |= Q(children=int(childCount))
        if childFilters:
            matches = matches.filter(childFilters)

    filters = {}
    for field, lookup in MATRIMONIAL_PROFILE_FIELD_FILTERS.items():
        value = getattr(preference, field, None)
        if value and ANY_PREFERENCE not in value:
            filters[lookup] = value

    for field, lookup in MATRIMONIAL_PROFILE_BOOLEAN_FIELD_FILTERS.items():
        value = getattr(preference, field, None)
        if value and ANY_PREFERENCE not in value:
            filters[lookup] = value[0] == 'YES'

    if filters:
        matches = matches.filter(**filters)
    return matches


def getMatchesLookingForYou(user):
    matches = getBaseMatches(user).filter(user__partnerPreference__isnull=False)
    user = get_user_model().objects.select_related(*USER_PROFILE_RELATIONS).get(pk=user.pk)

    matrimonial = getattr(user, 'matrimonialProfile', None)
    religious = getattr(user, 'religiousProfile', None)
    education = getattr(user, 'educationProfile', None)
    career = getattr(user, 'careerProfile', None)
    location = getattr(user, 'locationProfile', None)
    family = getattr(user, 'familyProfile', None)

    myAge = matrimonial.age if matrimonial else None
    myHeight = matrimonial.height if matrimonial else None

    myStatus = {
        'maritalStatus': matrimonial.maritalStatus if matrimonial else None,
        'children': matrimonial.children if matrimonial else None,
        'nationality': matrimonial.nationality if matrimonial else None,
        'physicalStatus': matrimonial.physicalStatus if matrimonial else None,
        'eatingHabit': matrimonial.eatingHabit if matrimonial else None,
        'smokingHabit': matrimonial.smokingHabit if matrimonial else None,
        'languages': matrimonial.languages if matrimonial else None,
        'residency': location.residency if location else None,
        'citizenship': location.citizenShip if location else None,
        'educationLevel': education.educationLevel if education else None,
        'employmentStatus': career.employmentStatus if career else None,
        'industry': career.industry if career else None,
        'madhab': religious.madhab if religious else None,
        'prayerFrequency': religious.prayerFrequency if religious else None,
        'quranReading': religious.quranReading if religious else None,
        'observesFasting': (
            'YES' if religious.observesFasting is True
            else 'NO' if religious.observesFasting is False
            else None
        ) if religious else None,
        'familyStatus': family.familyStatus if family else None,
        'familyType': family.familyType if family else None,
        'familyValue': family.familyValue if family else None,
    }

    if myAge is not None:
        matches = matches.filter(
            Q(user__partnerPreference__minAge__isnull=True) |
            Q(user__partnerPreference__minAge__lte=myAge),
            Q(user__partnerPreference__maxAge__isnull=True) |
            Q(user__partnerPreference__maxAge__gte=myAge),
        )

    if myHeight is not None:
        matches = matches.filter(
            Q(user__partnerPreference__minHeight__isnull=True) |
            Q(user__partnerPreference__minHeight__lte=myHeight),

            Q(user__partnerPreference__maxHeight__isnull=True) |
            Q(user__partnerPreference__maxHeight__gte=myHeight),
        )

    preferenceModel = user.partnerPreference.__class__
    preferenceTable = preferenceModel._meta.db_table

    def matchesJSONPreference(queryset, field, myValue):
        if myValue is None or myValue == '' or myValue == []:
            return queryset

        values = list(myValue) if isinstance(myValue, (list, tuple)) else [myValue]
        values = [
            str(value)
            for value in values
            if value not in (None, '')
        ]

        if not values:
            return queryset

        if field == 'children':
            childCount = int(myValue)
            values = [str(childCount)]

            if childCount >= 5:
                values.append(FIVE_OR_MORE_CHILDREN)

        column = f'"{preferenceTable}"."{field}"'
        placeholders = ', '.join(['%s'] * len(values))
        sql = f"""
            (
                {column} IS NULL

                OR json_array_length({column}) = 0

                OR EXISTS (
                    SELECT 1
                    FROM json_each({column}) AS preference
                    WHERE
                        preference.value = %s

                        OR preference.value IN ({placeholders})
                )
            )
        """
        params = [ANY_PREFERENCE, *values]

        return queryset.extra(where=[sql], params=params)

    for field, myValue in myStatus.items():
        matches = matchesJSONPreference(matches, field, myValue)

    return matches.distinct()


def getMatchesNonSmokers(user):
    return getBaseMatches(user).filter(smokingHabit=SmokingHabit.NON_SMOKER)


def getMatchesWillingToRelocate(user):
    return getBaseMatches(user).filter(locationProfile__willingToRelocate=True)


def registerProfileView(viewer, viewed):
    view = ProfileView.objects.filter(viewer=viewer, viewed=viewed).update(viewedAt=timezone.now())
    if not view:
        ProfileView.objects.create(viewer=viewer, viewed=viewed)


MATCHES_FILTER_FUNCTIONS = {
    'viewed-you': getMatchesViewedUser,
    'viewed-by-you': getMatchesViewedByUser,
    'newly-joined': getMatchesJoinedRecently,
    'verified': getMatchesVerified,
    'recently-active': getMatchesRecentlyActive,
    'created-by-family': getMatchesCreatedByParentOrRelative,
    'single': getMatchesSingle,
    'divorced': getMatchesDivorced,
    'widowed': getMatchesWidowed,
    'no-children': getMatchesWithoutChildren,
    'with-children': getMatchesWithChildren,
    'age-18-25': getMatchesBetween18And25,
    'age-26-35': getMatchesBetween26And35,
    'age-36-plus': getMatches36AndAbove,
    'mutual': getMatchesMatchingMyPreference,
    'looking-for-you': getMatchesLookingForYou,
    'madhab': getMatchesByMadhab,
    'prayer': getMatchesByPrayerFrequency,
    'eating': getMatchesByEatingHabit,
    'education': getMatchesByEducation,
    'non-smoker': getMatchesNonSmokers,
    'relocate': getMatchesWillingToRelocate,
}
