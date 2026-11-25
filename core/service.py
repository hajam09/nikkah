from calendar import monthrange
from datetime import timedelta

from django.utils import timezone

from core.choices import Gender, CreatedBy, MaritalStatus, SmokingHabit
from core.constants import MATRIMONIAL_PROFILE_RELATIONS
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
    return getBaseMatches(user).filter(numberOfChildren=0)


def getMatchesWithChildren(user):
    return getBaseMatches(user).filter(numberOfChildren__gt=0)


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

    if not madhabList or '__ANY__' in madhabList:
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

    if not prayerFrequencyList or '__ANY__' in prayerFrequencyList:
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

    if not eatingHabitList or '__ANY__' in eatingHabitList:
        return matches
    return matches.filter(eatingHabit__in=eatingHabitList)


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
    'madhab': getMatchesByMadhab,
    'prayer': getMatchesByPrayerFrequency,
    'eating': getMatchesByEatingHabit,
    'non-smoker': getMatchesNonSmokers,
    'relocate': getMatchesWillingToRelocate,
}
